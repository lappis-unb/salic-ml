# %load csver.py

# %load app.py
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime

from IPython.display import display
import string


class CSVer:

    DATE_INPUT_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_OUTPUT_FORMAT = '%m/%Y'
    DATE_GRAPH_FORMAT = DATE_OUTPUT_FORMAT

    def __init__(self, csv_names):
        self.csvs = list(map(pd.read_csv, csv_names))

    def get_distinct_rows(self, column_name, csv_pos=0):
        csv = self.csvs[csv_pos]
        distinct_rows = csv[column_name].unique()
        return distinct_rows

    def filter_column_by_value(self, column, value, csv_pos=0):
        csv = self.csvs[csv_pos]
        return csv[csv[column] == value]

    def get_date_axis_from_column(self, data_frame=None,
                                  column='Data', csv_pos=0):
        if data_frame is None:
            data_frame = self.csvs[csv_pos]

        dates = data_frame[column].values
        dates_date_time = [datetime.strptime(
            d, CSVer.DATE_INPUT_FORMAT) for d in dates]
        dates_axis = matplotlib.dates.date2num(dates_date_time)
        return dates_axis

    def get_random_item(self, column, csv_pos=0):
        distinct_items = self.get_distinct_rows(column, csv_pos)
        item = np.random.choice(distinct_items)
        return item

    def get_x_y(self, x_column, y_column, filter=None, csv_pos=0):
        rows = None
        if filter is not None:
            column, value = filter
            rows = self.filter_column_by_value(column, value, csv_pos)
        else:
            rows = self.csvs[csv_pos]

        x = np.array(rows[x_column].values)
        y = np.array(rows[y_column].values)
        return (x, y)

    def get_date_axis_from_array(self, dates):
        dates_date_time = [datetime.strptime(
            d, CSVer.DATE_INPUT_FORMAT) for d in dates]
        dates_axis = matplotlib.dates.date2num(dates_date_time)
        return dates_axis


if __name__ == '__main__':
    solicitado = 'solicitado_small.csv'
    aprovado = 'aprovado_small.csv'

    l = [solicitado, aprovado]
    csver = CSVer(l)
    dt = csver.get_random_item('Item', 0)
    display(dt)
