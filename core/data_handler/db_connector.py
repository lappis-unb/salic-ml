import os

import pandas as pd
import pyodbc as dbc


class DbConnector:

    def __init__(self):
        self._database_connect()

    def __del__(self):
        self._database_disconnect()

    def _database_connect(self):
        db_credentials = {
            'HOST': os.environ.get('DB_HOST', ''),
            'PORT': os.environ.get('DB_PORT', ''),
            'USER': os.environ.get('DB_USER', ''),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'DATABASE': os.environ.get('DB_NAME', ''),
        }

        db_parameters = (
            'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};\
             TDS_Version=8.0;'
            .format(db_credentials['HOST'], db_credentials['PORT'],
                    db_credentials['USER'], db_credentials['PASSWORD'])
        )

        self.db = dbc.connect(db_parameters)

    def _database_disconnect(self):
        self.db.close()

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        ret = cursor.fetchall()
        cursor.close()
        return ret

    def execute_pandas_sql_query(self, query, chunksize=None):
        dataframe = pd.read_sql_query(query, self.db, coerce_float=False, chunksize=chunksize)
        return dataframe

