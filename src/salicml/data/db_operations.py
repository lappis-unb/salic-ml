import os
import pathlib
from .db_connector import db_connector
from salicml.data.loader import WRITE_DF, WRITE_DF_OPTS, FILE_EXTENSION

SQL_EXTENSION = ".sql"
DATA_PATH = pathlib.Path(__file__).parent.parent.parent.parent / "data"


def test_connection():
    db = db_connector()
    print('aee')
    data = db.execute_query("SELECT * FROM BDCORPORATIVO.scSAC.tbItemCusto")
    db.close()
    return data


def save_dataframe_as_pickle(df, dir_path):
    if os.path.exists(dir_path):
        answer = input('Overwrite file/dir \'{}\'?[y/N] '.format(dir_path))
        if answer != 'y':
            exit('Abort.')

    dirname = os.path.dirname(dir_path)
    if not os.path.exists(os.path.dirname(dir_path)):
        os.makedirs(dirname)

    WRITE_DF(df, dir_path, **WRITE_DF_OPTS)
    print('pickle saved in path \'{}\'.'.format(dir_path))


def save_sql_to_files():
    """
    Executes every .sql files in /data/scripts/ using salic db vpn and then saves
    pickle files into /data/raw/
    """
    ext_size = len(SQL_EXTENSION)
    for file in os.listdir(DATA_PATH / 'scripts'):
        with open(file, 'r') as file_content:
            query = file_content.read()
            sql_filename = os.path.basename(file)
            print('Downloading query [{}]...'.format(sql_filename))
            db = db_connector()
            query_result = db.execute_pandas_sql_query(query)
            db.close()
            save_dir = DATA_PATH / "raw"
            file_path = os.path.join(save_dir,
                                     file[:-ext_size] + '.' + FILE_EXTENSION)
            save_dataframe_as_pickle(query_result, file_path)
