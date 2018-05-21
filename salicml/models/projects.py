import pandas as pd


class Projects:

    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path

        self.data_frame = pd.read_csv(csv_file_path, low_memory = False)

    def get_data_frame_columns(self, cols):
        return self.data_frame.filter(items = cols)
