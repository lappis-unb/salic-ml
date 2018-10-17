import os
from core.data_handler import storage
from core.data_handler.db_connector import DbConnector


class DataSource:

    DATA_SOURCE_DIR = os.path.dirname(os.path.realpath(__file__))

    CACHE_DIR_NAME = 'cache'
    CACHE_EXTENSION = '.pickle'
    CACHE_DIR_PATH = os.path.join(DATA_SOURCE_DIR, CACHE_DIR_NAME)

    def __init__(self, sql_file_path):
        self.file_path = sql_file_path
        self.file_name = os.path.basename(sql_file_path)

        self._init_map_where()

    def _init_map_where(self):
        self.map_where = {}

        mp = self.map_where
        mp['planilha_captacao.sql'] = 'WHERE (capt.AnoProjeto+capt.Sequencial)'
        mp['planilha_comprovacao.sql'] = 'AND (projetos.AnoProjeto + projetos.Sequencial)'
        mp['planilha_orcamentaria.sql'] = 'WHERE a.PRONAC'
        mp['planilha_projetos.sql'] = 'WHERE (projetos.AnoProjeto + projetos.Sequencial)'



    def get_dataset(self, pronac=None, use_cache=False):
        download = True
        dataset = None
        cache_name = self.file_name[:-4] + DataSource.CACHE_EXTENSION
        cache_path = os.path.join(DataSource.CACHE_DIR_PATH, cache_name)


        if (not pronac) and use_cache:
            print('cache_path = {}'.format(cache_path))

            if os.path.exists(cache_path):
                download = False
                dataset = storage.load(cache_path, on_error_callback=None)

        if download:
            db_connector = DbConnector()
            sql = self._prepare_sql(pronac)

            dataset = db_connector.execute_pandas_sql_query(sql)
            if False:#not pronac:
                storage.save(cache_path, dataset)

        print('\ndataset = \n')
        print(dataset)

        assert not dataset.empty
        return dataset



    def _prepare_sql(self, pronac):
        with open(self.file_path) as sql_file:
            sql = sql_file.read()
            if pronac:
                column = self.map_where[self.file_name]
                sql += '{}=\'{}\''.format(column, pronac)
            return sql


