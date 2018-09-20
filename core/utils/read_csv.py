import pandas as pd
import os


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_ROOT = os.path.join(FILE_PATH, os.pardir, os.pardir)
DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data', 'raw')


def read_csv(csv_name, usecols=None):
    """Returns a DataFrame from a .csv file stored in /data/raw/"""
    csv_path = os.path.join(DATA_FOLDER, csv_name)
    csv = pd.read_csv(csv_path, low_memory=False, usecols=usecols,
            encoding='utf-8')
    return csv


def read_csv_with_different_type(csv_name, column_types_dict, usecols=None):
    """Returns a DataFrame from a .csv file stored in /data/raw/.
    Reads the CSV as string. """
    csv_path = os.path.join(DATA_FOLDER, csv_name)
    csv = pd.read_csv(csv_path, usecols=usecols, encoding='utf-8',
            dtype=column_types_dict, engine='python')

    for key_column, val_type in column_types_dict.items():
        if (val_type == str):
            csv[key_column] = csv[key_column].str.strip() # str.replace(' ', '')

    return csv

def read_csv_as_integer(csv_name, integer_columns,usecols=None):
    """Returns a DataFrame from a .csv file stored in /data/raw/.
    Converts columns specified by 'integer_columns' to integer.
    """
    csv_path = os.path.join(DATA_FOLDER, csv_name)
    csv = pd.read_csv(csv_path, low_memory=False, usecols=usecols)
    for column in integer_columns:
        csv = csv[pd.to_numeric(csv[column], errors='coerce').notnull()]
    csv[integer_columns] = csv[integer_columns].apply(pd.to_numeric)
    return csv
