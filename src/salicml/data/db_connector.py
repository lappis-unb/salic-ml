import os

import pandas as pd
import pymssql


class DbConnector:
    def __init__(self):
        self._database_connect()

    def _database_connect(self):
        db_credentials = {
            "HOST": os.environ.get("CONNECT_DB_HOST", ""),
            "PORT": os.environ.get("CONNECT_DB_PORT", ""),
            "USER": os.environ.get("CONNECT_DB_USER", ""),
            "PASSWORD": os.environ.get("CONNECT_DB_PASSWORD", ""),
            "DATABASE": os.environ.get("CONNECT_DB_NAME", ""),
        }

        self.db = pymssql.connect(host=db_credentials["HOST"],
                                  user=db_credentials["USER"],
                                  password=db_credentials["PASSWORD"],
                                  database=db_credentials["DATABASE"],
                                  port=db_credentials["PORT"])

    def _database_disconnect(self):
        self.db.close()

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def execute_pandas_sql_query(self, query, chunksize=None):
        dataframe = pd.read_sql_query(
            query, self.db, coerce_float=False, chunksize=chunksize
        )
        return dataframe

    def close(self):
        self._database_disconnect()


db_connector = DbConnector
