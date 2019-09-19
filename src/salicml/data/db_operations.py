import os
import pathlib
import pandas as pd
import gc
from .db_connector import db_connector
from .loader import WRITE_DF, WRITE_DF_OPTS, FILE_EXTENSION

SQL_EXTENSION = ".sql"
DATA_PATH = pathlib.Path(__file__).parent.parent.parent.parent / "data"


def chunk_writer(chunk, path):
    existent_df = pd.DataFrame.empty()
    if os.path.exists(path):
        existent_df = pd.read_pickle(path)

    result_df = pd.concat(existent_df, chunk)
    WRITE_DF(result_df, path, **WRITE_DF_OPTS)


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


def save_sql_to_files(overwrite=False):
    """
    Executes every .sql files in /data/scripts/ using salic db vpn and
    then saves pickle files into /data/raw/
    """
    ext_size = len(SQL_EXTENSION)
    path = DATA_PATH / 'scripts'
    save_dir = DATA_PATH / "raw"

    for file in os.listdir(path):
        if file.endswith(SQL_EXTENSION):
            file_path = os.path.join(save_dir,
                                     file[:-ext_size] + '.' + FILE_EXTENSION)
            if not os.path.isfile(file_path) or overwrite:
                query_result = make_query(path / file)
                save_dataframe_as_pickle(query_result, file_path)
            else:
                print(("file {} already exists, if you would like to update"
                       " it, use -f flag\n").format(file_path))


def save_sql_to_file(sql, dest):
    #query_result = make_query(sql)
    ext_size = len(SQL_EXTENSION)
    file_name = os.path.basename(sql)
    file_path = os.path.join(dest,
                             file_name[:-ext_size] + '.' + FILE_EXTENSION)
    #save_dataframe_as_pickle(query_result, file_path)
    make_chunk_query(sql, file_path)


def make_query(sql_file):
    with open(sql_file, 'r') as file_content:
        query = file_content.read()
        sql_filename = os.path.basename(sql_file)
        print('Downloading query [{}]...'.format(sql_filename))
        db = db_connector()
        query_result = db.execute_pandas_sql_query(query)
        db.close()
        return query_result

def make_chunk_query(sql_file, path): 
    with open(sql_file, 'r') as file_content:
        query = file_content.read()
        sql_filename = os.path.basename(sql_file)
        print('Downloading query [{}]...'.format(sql_filename))
        db = db_connector()
        for c in db.execute_pandas_sql_query(query, chunksize=1000):
            chunk_writer(c, path)
            gc.collect()
        db.close()

