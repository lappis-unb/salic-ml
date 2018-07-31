from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib


class Dates:

    DATE_INPUT_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_OUTPUT_FORMAT = '%m/%Y'
    DATE_GRAPH_FORMAT = DATE_OUTPUT_FORMAT

    @staticmethod
    def get_date_axis_from_column(data, column='Data'):
        dates = data[column]
        dates_date_time = None
        date_cell_type = dates.dtype
        if date_cell_type == 'str':
            dates_date_time = [datetime.strptime(
                d, Dates.DATE_INPUT_FORMAT) for d in dates]
        elif np.issubdtype(date_cell_type, np.datetime64):
            dates_date_time = dates
        else:
            raise TypeError('Date type not supported')
        dates_axis = matplotlib.dates.date2num(dates_date_time)
        return dates_axis

    @staticmethod
    def get_xy(data, x_column, y_column):
        x = data[x_column].values
        y = data[y_column].values
        return (x, y)

    @staticmethod
    def get_xy_dates(data, data_column, y_column):
        x = Dates.get_date_axis_from_column(data, data_column)
        return (x, data[y_column])
