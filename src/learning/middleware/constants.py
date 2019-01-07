import os


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
SQL_FOLDER = os.path.join(FILE_PATH, os.pardir, "data_source", "sql_scripts")
TRAIN_FOLDER = os.path.join(FILE_PATH, "trainings")
