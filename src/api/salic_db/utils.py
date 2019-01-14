import pyodbc
import os

SALIC_CREDENTIALS = {
    'HOST': os.environ.get('SALIC_DB_HOST', ''),
    'PORT': os.environ.get('SALIC_DB_PORT', ''),
    'USER': os.environ.get('SALIC_DB_USER', ''),
    'PASSWORD': os.environ.get('SALIC_DB_PASSWORD', ''),
    'DATABASE': os.environ.get('SALIC_DB_NAME', ''),
}


def test_connection():
    db_parameters = 'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};TDS_Version=8.0;'.format(SALIC_CREDENTIALS['HOST'], SALIC_CREDENTIALS['PORT'], SALIC_CREDENTIALS['USER'], SALIC_CREDENTIALS['PASSWORD'])
    db = pyodbc.connect(db_parameters)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM BDCORPORATIVO.scSAC.tbItemCusto")
    data = cursor.fetchone()
    db.close()
    return data

def make_query_from_db(query):
    db_parameters = 'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};TDS_Version=8.0;'.format(SALIC_CREDENTIALS['HOST'], SALIC_CREDENTIALS['PORT'], SALIC_CREDENTIALS['USER'], SALIC_CREDENTIALS['PASSWORD'])
    db = pyodbc.connect(db_parameters)
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return data
