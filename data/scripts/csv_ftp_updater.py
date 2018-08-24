#!/usr/bin/env python

import argparse
import os
import sys

import pandas as pd
import pyodbc

from ftplib import FTP

CREDENTIALS = {
    'HOST': os.environ.get('DB_HOST', ''),
    'PORT': os.environ.get('DB_PORT', ''),
    'USER': os.environ.get('DB_USER', ''),
    'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    'DATABASE': os.environ.get('DB_NAME', ''),
    'FTP_USER': os.environ.get('FTP_USER', ''),
    'FTP_PASSWORD': os.environ.get('FTP_PASSWORD', ''),
}

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

def execute_pandas_sql_query(query):
    '''Executes SQL query, returns the result as a DataFrame object.'''
    db_parameters = 'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};TDS_Version=8.0;'.format(CREDENTIALS['HOST'], CREDENTIALS['PORT'], CREDENTIALS['USER'], CREDENTIALS['PASSWORD'])

    db_conection = pyodbc.connect(db_parameters)
    dataframe = pd.read_sql_query(query, db_conection)
    db_conection.close()

    return dataframe

def save_dataframe_as_csv(dt, dir_path):
    if not isinstance(dt, pd.DataFrame):
        raise ValueError('dt argument must be a ' \
                '{}'.format(pd.DataFrame.__name__))

    if os.path.exists(dir_path):
        answer = input('Overwrite file/dir \'{}\'?[y/N] '.format(dir_path))
        if answer != 'y':
            exit('Abort.')

    dirname = os.path.dirname(dir_path)
    if not os.path.exists(os.path.dirname(dir_path)):
        os.makedirs(dirname)

    dt.to_csv(dir_path, index=False)
    print('.csv saved in path \'{}\'.'.format(dir_path))

def save_file_in_ftp(ftp, source_file_path, dest_file_path):
    dest_filename = os.path.basename(dest_file_path)
    dest_dirname = os.path.dirname(dest_file_path)
    ftp.cwd(dest_dirname)
    with open(source_file_path, 'rb') as f_send:
        ftp.storbinary('STOR {}'.format(dest_filename), f_send)
        ftp.sendcmd('SITE CHMOD 644 ' + dest_filename)
        print('File \'{}\' saved in \'ftp/{}\''.format(source_file_path,
            dest_file_path))

def init_ftp():
    host = '178.128.12.141'
    user = CREDENTIALS['FTP_USER']
    passwd = CREDENTIALS['FTP_PASSWORD']

    ftp = FTP(host)
    ftp.login(user, passwd)

    return ftp

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

    csv_paths = []
    for file_path in files:
        with open(file_path, 'r') as file_content:
            query = file_content.read()
            query_result = execute_pandas_sql_query(query)

            csv_path = os.path.join(csv_dir, file_path[:-4] + '.csv')
            save_dataframe_as_csv(query_result, csv_path)
            
            csv_paths.append(csv_path)
    
    ftp = init_ftp()

    update_ftp = args['update_ftp']
    if update_ftp:
        for csv_path in csv_paths:
            csv_filename = os.path.basename(csv_path)
            dest_file_path = 'raw/' + csv_filename
            save_file_in_ftp(ftp, csv_path, dest_file_path)

    ftp.quit()

if __name__ == '__main__':
    main()
