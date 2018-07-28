import pandas as pd
import os


PROJECT_ROOT = os.path.abspath(os.path.join(os.pardir, os.pardir))
DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data', 'raw')

def read_csv(csv_name):
    """Returns a DataFrame from a .csv file stored in /data/raw/"""
    csv_path = os.path.join(DATA_FOLDER, csv_name)
    csv = pd.read_csv(csv_path, low_memory=False)
    return csv
