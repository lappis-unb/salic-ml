from datetime import datetime
import matplotlib

class Dates:

    DATE_INPUT_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_OUTPUT_FORMAT = '%m/%Y'
    DATE_GRAPH_FORMAT = DATE_OUTPUT_FORMAT

    @staticmethod
    def get_date_axis_from_column(data, column = 'Data'):
        dates = data[column].values
        dates_date_time = [datetime.strptime(d, Dates.DATE_INPUT_FORMAT) for d in dates]
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
