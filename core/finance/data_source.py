import os


class DataSource:

    CACHE_FOLDER =

    def __init__(self, sql_file_path):
        self.file_path = sql_file_path
        self.file_name = os.path.basename(sql_file_path)

    def get_dataset(self, pronac=None, use_cache=False):
        download = True

        if(not pronac and use_cache):


