import pandas as pd
import os

from abc import ABC, abstractmethod
from salicml.data_source.db_connector import DbConnector
from salicml.middleware import constants
from salicml.utils import storage


class VerifiedApprovedDataSource:
    SQL_NAME = "planilha_aprovacao_comprovacao.sql"
    SQL_PATH = os.path.join(constants.SQL_FOLDER, SQL_NAME)

    def __init__(self):
        with open(VerifiedApprovedDataSource.SQL_PATH, "r") as sql_file:
            self.sql = sql_file.read()
        self.db_connector = DbConnector()

    def download_dataset(self, pronac=None):
        if pronac is None:
            query = self.sql
        else:
            where_pronac = (
                " AND (projetos.AnoProjeto + projetos.Sequencial)"
                "= {};".format(pronac)
            )
            query = self.sql.replace(";", where_pronac)

        dataset = self.db_connector.execute_query(query)
        return dataset


class DataSourceABC(ABC):
    """This class defines the interface that is responsable for getting raw
    data about SALIC projects from different sources."""

    @abstractmethod
    def get_planilha_orcamentaria(self, pronac="", columns=None, use_cache=False):
        """Returns the budgetary spreadsheet about SALIC projects. The output
        is a matrix, represented as a python list of python lists.

        Input example:
            [['PRONAC', 'idPlanilhaAprovacao', 'idSegmento']]

        Output example:
            [['123456', '2A', 123],
             ['123456', '2A', 124],
             ['123457', 'AA', 323],
             ['123458', 'XY', 923], ]
        """
        pass

    @abstractmethod
    def get_planilha_aprovacao_comprovacao(self, pronac=None):
        pass


class DataSourceDb(DataSourceABC):
    PATH = os.path.join(constants.TRAIN_FOLDER, "planilha_orcamentaria.pickle")

    def __init__(self):
        self.db_connector = DbConnector()

    def _read_cache(self):
        spreadsheet = storage.load(
            DataSourceDb.PATH, on_error_callback=self.no_cache_callback
        )
        return spreadsheet

    def no_cache_callback(self):
        raise FileNotFoundError("No file {}".format(DataSourceDb.PATH))

    def get_planilha_aprovacao_comprovacao(self, pronac=None):
        verified_approved_datasource = VerifiedApprovedDataSource()
        return verified_approved_datasource.download_dataset(pronac=pronac)

    def download_planilha_orcamentaria(self, columns=None, pronac=""):
        """'Returns [[PRONAC, id_planilha_aprovacao, id_segmento]]"""
        DB_COLUMN = {
            "PRONAC": "a.PRONAC",
            "idSegmento": "p.Segmento AS idSegmento",
            "idPlanilhaAprovacao": "a.idPlanilhaAprovacao",
        }

        if columns is None:
            columns = DB_COLUMN.keys()

        column_order = ["PRONAC", "idPlanilhaAprovacao", "idSegmento"]

        select = "SELECT "
        select += ",".join([DB_COLUMN[key] for key in column_order if key in columns])
        select += "\n"
        from_db = (
            "FROM SAC.dbo.vwPlanilhaAprovada a\n"
            "LEFT JOIN SAC.dbo.Projetos p\n"
            "ON a.idPronac = p.IdPRONAC\n"
            "INNER JOIN SAC.dbo.tbPlanilhaItens i\n"
            "ON Item = i.Descricao\n"
            "INNER JOIN SAC.dbo.Segmento s\n"
            "ON P.Segmento = s.Codigo\n"
            "INNER JOIN SAC.dbo.Area area\n"
            "ON p.Area = area.Codigo"
        )

        sql_query = select + from_db
        if pronac:
            where = "\n" + "WHERE a.PRONAC = '{0}'".format(pronac)
            sql_query += where
        sql_query += ";"

        spreadsheet = self.db_connector.execute_query(sql_query)
        return spreadsheet

    def get_planilha_orcamentaria(self, columns=None, pronac="", use_cache=False):
        download = True

        if use_cache and not pronac:
            try:
                spreadsheet = self._read_cache()
                download = False
            except FileNotFoundError:
                pass

        if download:
            spreadsheet = self.download_planilha_orcamentaria(
                columns=columns, pronac=pronac
            )
            storage.save(DataSourceDb.PATH, spreadsheet)

        return spreadsheet


class DataSourceMock(DataSourceABC):
    def __init__(self, planilha_orcamentaria=None):
        self._planilha_orcamentaria = pd.DataFrame(planilha_orcamentaria)

    def get_planilha_orcamentaria(self, columns=None, pronac="", use_cache=False):
        df = self._planilha_orcamentaria
        spreadsheet = None
        if pronac:
            spreadsheet = df[df[0] == pronac]
        else:
            spreadsheet = df
        spreadsheet = spreadsheet.values.tolist()
        return spreadsheet

    def set_planilha_aprovacao_comprovacao(self, dataset):

        items_df = pd.DataFrame(dataset)
        items_df.columns = items_df.iloc[0].values
        items_df = items_df[1:]
        self.planilha_aprovacao_comprovacao = items_df

    def get_planilha_aprovacao_comprovacao(self, pronac=None):
        if pronac is None:
            result = self.planilha_aprovacao_comprovacao
        else:
            df = self.planilha_aprovacao_comprovacao
            result = df[df["PRONAC"] == pronac]
        return result
