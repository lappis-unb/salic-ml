import matplotlib
import matplotlib.pyplot as plt

import warnings
import matplotlib.cbook


from salicml.utils.dates import Dates

#
#
# warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#


class Plotter:

    @staticmethod
    def plot_histogram(y_axis, x_label='', y_label='', title=''):
        fig = plt.figure()
        Plotter.set_plot_style(x_label, y_label, title)

        result = plt.hist(y_axis, bins='fd', color='blue',
                          edgecolor='black', alpha=.75)
        return result

    @staticmethod
    def set_plot_style(x_label, y_label, title):
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)

    @staticmethod
    def plot_scatter_along_time(x_axis, y_axis, color=None, x_label='',
                                y_label='', title='', marker='o', subplot=111,
                                figure=None):

        if figure is None:
            figure = plt.figure()

        hfmt = matplotlib.dates.DateFormatter(Dates.DATE_GRAPH_FORMAT)
        ax = figure.add_subplot(subplot)
        ax.xaxis.set_major_formatter(hfmt)
        ax.xaxis_date()
        plt.setp(ax.get_xticklabels(), rotation=45)
        Plotter.set_plot_style(x_label, y_label, title)

        plt.scatter(x_axis, y_axis, s=50, c=color, alpha=0.50, marker=marker)

    @staticmethod
    def plot_log_along_time(x_axis, y_axis, format='g.', x_label='', y_label='',
                            title='', subplot=111, figure=None):
        if figure is None:
            figure = plt.figure()

        hfmt = matplotlib.dates.DateFormatter(Dates.DATE_GRAPH_FORMAT)
        ax = figure.add_subplot(subplot)
        ax.xaxis.set_major_formatter(hfmt)
        plt.setp(ax.get_xticklabels(), rotation=45)
        plt.semilogy(x_axis, y_axis, format)
        Plotter.set_plot_style(x_label, y_label, title)
#
#    def plot_scatter_log_along_time(self, x_axis, y_axis, x_label = '',
#                                    y_label = '', title = ''):
#        figure = plt.figure()
#        self.plot_scatter_along_time(x_axis, y_axis, x_label, y_label,
#                                     title, subplot = 121,
#                                     figure = figure)
#        self.plot_log_along_time(x_axis, y_axis, x_label, y_label,
#                                 title, subplot = 122,
#                                 figure = figure)
#
#
#

    def show():
        plt.show()
