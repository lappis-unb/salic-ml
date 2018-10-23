import os

from core.data_handler import storage
from core.data_handler.db_connector import DbConnector
from core.utils.exceptions import DataNotFoundForPronac


class DataSource:

    DATA_SOURCE_DIR = os.path.dirname(os.path.realpath(__file__))

    CACHE_DIR_NAME = 'cache'
    CACHE_EXTENSION = '.pickle'
    CACHE_DIR_PATH = os.path.join(DATA_SOURCE_DIR, CACHE_DIR_NAME)

    def __init__(self):
        self._init_map_where()

    def _init_map_where(self):
        self.map_where = {}

        mp = self.map_where
        mp['planilha_captacao.sql'] = 'WHERE (capt.AnoProjeto+capt.Sequencial)'
        mp['planilha_comprovacao.sql'] = ' AND (projetos.AnoProjeto + projetos.Sequencial)'
        mp['planilha_orcamentaria.sql'] = 'AND (a.AnoProjeto+a.Sequencial)'
        mp['planilha_projetos.sql'] = 'WHERE (projetos.AnoProjeto + projetos.Sequencial)'

    def get_dataset(self, sql_file_path, pronac=None, use_cache=False):
        file_name = os.path.basename(sql_file_path)

        download = True
        dataset = None
        cache_name = file_name[:-4] + DataSource.CACHE_EXTENSION
        cache_path = os.path.join(DataSource.CACHE_DIR_PATH, cache_name)

        if (not pronac) and use_cache:
            if os.path.exists(cache_path):
                download = False
                dataset = storage.load(cache_path, on_error_callback=None)

        if download:
            db_connector = DbConnector()
            sql = self._prepare_sql(sql_file_path, pronac)
            dataset = db_connector.execute_pandas_sql_query(sql)

            if not pronac:
                storage.save(cache_path, dataset)
        else:
            print('Cache "{}" was used for {}\n'.format(cache_path, file_name))

        if pronac and dataset.empty:
            raise DataNotFoundForPronac

        for column in dataset.columns:
            if column.lower().replace(' ', '') == 'pronac':
                dataset[column] = dataset[column].str.replace(' ', '')

        assert not dataset.empty
        return dataset

    def _prepare_sql(self, sql_file_path, pronac):
        file_name = file_name = os.path.basename(sql_file_path)

        with open(sql_file_path) as sql_file:
            sql = sql_file.read()
            if pronac:
                column = self.map_where[file_name]
                sql += '{}=\'{}\''.format(column, pronac)
            return sql


