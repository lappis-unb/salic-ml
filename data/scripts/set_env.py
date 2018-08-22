#!/usr/bin/env python

import os
import sys

import pyodbc

debug = lambda a, b: print('{} = {}'.format(a, b))

CREDENTIALS = {
    'HOST': os.environ.get('DB_HOST', ''),
    'PORT': os.environ.get('DB_PORT', ''),
    'USER': os.environ.get('DB_USER', ''),
    'PASSWORD': os.environ.get('DB_PASSWORD', ''),
    'DATABASE': os.environ.get('DB_NAME', ''),
}

def make_query_from_db(query):
    db_parameters = 'DRIVER=FreeTDS;SERVER={0};PORT={1};DATABASE=;UID={2};PWD={3};TDS_Version=8.0;'.format(CREDENTIALS['HOST'], CREDENTIALS['PORT'], CREDENTIALS['USER'], CREDENTIALS['PASSWORD'])
    debug('db_parameters', db_parameters)

    db = pyodbc.connect(db_parameters)
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    db.close()
    return data


def main():
    USAGE = 'usage: python {} <filelist | dirlist>'.format(__file__)

    args = sys.argv
    if len(args) == 1:
        print(USAGE)
        exit(1)

    paths = args[1:]
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
            print('Ignoring non .sql file {}'.format(path))

    for file_path in files:
        with open(file_path, 'r') as file_content:
            query = file_content.read()
            query_result = make_query_from_db(query)
            debug('query_result', query_result)

    debug('files', files)

if __name__ == '__main__':
    main()
