#!/usr/bin/env python

import argparse
import os
import sys

import pandas as pd
import pyodbc


def debug(a, b):
    print('{} = {}'.format(a, b))
    print('type({}) = {}'.format(a, type(b)))

CREDENTIALS = {
    'HOST': os.environ.get('DB_HOST', ''),
    'PORT': os.environ.get('DB_PORT', ''),
    'USER': os.environ.get('DB_USER', ''),
    'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    'DATABASE': os.environ.get('DB_NAME', ''),
}

def execute_pandas_sql_query(query):
    '''Executes SQL query, returns the result as a DataFrame object.'''
    db_parameters = 'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};TDS_Version=8.0;'.format(CREDENTIALS['HOST'], CREDENTIALS['PORT'], CREDENTIALS['USER'], CREDENTIALS['PASSWORD'])

    db_conection = pyodbc.connect(db_parameters)
    dataframe = pd.read_sql_query(query, db_conection)
    db_conection.close()

    return dataframe

def set_and_parse_args():
    DESCRIPTION = 'Executes SQL Queries on SALIC database, ' \
                  'store the results as .csv files. Optionally, ' \
                  'you can update SALIC ftp server with the downloaded ' \
                  'data' \

    parse = argparse.ArgumentParser(description=DESCRIPTION)

    parse.add_argument('paths', nargs='*', help='List of .sql files or dirs ' \
            'that contain .sql files. Not recursive.')

    parse.add_argument('--csv_dir', help='Folder where .csv files will be ' \
            'saved.', default='.')

    parse.add_argument('--update_ftp', help='If present, all downloaded .csv files ' \
                       'will be saved in the ftp dir /raw/.',
                       action='store_true', default=False)
    args = parse.parse_args()
    args_dict = vars(args)
    return args_dict

def save_dataframe_as_csv(dt, dir_path):
    if not isinstance(dt, pd.DataFrame):
        raise ValueError('dt argument must be a ' \
                '{}'.format(pd.DataFrame.__name__))

    if os.path.exists(dir_path):
        answer = input('Overwrite file/dir \'{}\'?[y/N]'.format(dir_path))
        if answer != 'y':
            exit('Abort.')

    dirname = os.path.dirname(dir_path)
    if not os.path.exists(os.path.dirname(dir_path)):
        os.makedirs(dirname)

    dt.to_csv(dir_path, encoding='utf-8')
    print('.csv saved in file path \'{}\'.'.format(dir_path))

def main():
    args = set_and_parse_args()

    paths = args['paths']
    csv_dir = args['csv_dir']
    files = []

    for path in paths:
        if os.path.isdir(path):
            dir_files = [os.path.join(path, file_name)
                         for file_name in os.listdir(path)
                         if file_name.endswith('.sql')]
            paths += dir_files
        elif path.endswith('.sql'):
            files.append(path)
        else:
            print('Ignoring non-sql file {}'.format(path))

    for file_path in files:
        with open(file_path, 'r') as file_content:
            query = file_content.read()
            query_result = execute_pandas_sql_query(query)

            csv_path = os.path.join(csv_dir, file_path[:-4] + '.csv')
            save_dataframe_as_csv(query_result, csv_path)

if __name__ == '__main__':
    main()
