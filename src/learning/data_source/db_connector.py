import os
import pyodbc


class DbConnector:
    def __init__(self):
        self._database_connect()

    def __del__(self):
        self._database_disconnect()

    def _database_connect(self):
        db_credentials = {
            "HOST": os.environ.get("DB_HOST", ""),
            "PORT": os.environ.get("DB_PORT", ""),
            "USER": os.environ.get("DB_USER", ""),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "DATABASE": os.environ.get("DB_NAME", ""),
        }

        db_parameters = "DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};\
             TDS_Version=8.0;".format(
            db_credentials["HOST"],
            db_credentials["PORT"],
            db_credentials["USER"],
            db_credentials["PASSWORD"],
        )

        self.db = pyodbc.connect(db_parameters)

    def _database_disconnect(self):
        self.db.close()

    def execute_query(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        data = list(map(list, cursor.fetchall()))
        columns = [column[0] for column in cursor.description]
        table = [columns] + data
        cursor.close()

        return table
