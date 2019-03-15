import os
import pathlib
from .db_connector import db_connector
from .loader import WRITE_DF, WRITE_DF_OPTS, FILE_EXTENSION

SQL_EXTENSION = ".sql"
DATA_PATH = pathlib.Path(__file__).parent.parent.parent.parent.parent / "data"


def test_connection():
    db = db_connector()
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
    Executes every .sql files in /data/scripts/ using salic db vpn and
    then saves pickle files into /data/raw/
    """
    ext_size = len(SQL_EXTENSION)
    path = DATA_PATH / 'scripts'
    for file in os.listdir(path):
        query_result = make_query(path / file)
        save_dir = DATA_PATH / "raw"
        file_path = os.path.join(save_dir,
                                 file[:-ext_size] + '.' + FILE_EXTENSION)
        save_dataframe_as_pickle(query_result, file_path)


def save_sql_to_file(sql, dest):
    query_result = make_query(sql)
    ext_size = len(SQL_EXTENSION)
    file_name = os.path.basename(sql)
    file_path = os.path.join(dest,
                             file_name[:-ext_size] + '.' + FILE_EXTENSION)
    save_dataframe_as_pickle(query_result, file_path)


def make_query(sql_file):
    with open(sql_file, 'r') as file_content:
        query = file_content.read()
        sql_filename = os.path.basename(sql_file)
        print('Downloading query [{}]...'.format(sql_filename))
        db = db_connector()
        query_result = db.execute_pandas_sql_query(query)
        db.close()
        return query_result
