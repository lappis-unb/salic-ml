import os
from datetime import datetime
from operator import itemgetter

import pandas as pd
import numpy as np

from salicml.utils.utils import debug
from salicml.utils.dates import Dates


class ProjectItems:

    ID_PRONAC = 'idPronac'
    ID_ITEM = 'idPlanilhaItens'
    ITEM = 'Item'
    AREA = 'Area'
    SEGMENTO = 'Segmento'

    def __init__(self, data):
        self.dt = data

    def get_rows_by_column_value(self, column, value, dt=None):
        if dt is None:
            return self.dt[self.dt[column] == value]
        else:
            return dt[dt[column] == value]

    def items(self, id_pronac, dt=None):
        data = self.get_rows_by_column_value(ProjectItems.ID_PRONAC,
                                             id_pronac, dt=dt)
        return data[ProjectItems.ID_ITEM].unique()

    def areas_id(self, id_pronac):
        data = self.get_rows_by_column_value(ProjectItems.ID_PRONAC,
                                             id_pronac)
        res = (data.iloc[0].Area, data.iloc[0].Segmento)
        return res

    def all_areas(self):
        return self.unique_in_column(ProjectItems.AREA)

    def all_segments(self):
        return self.unique_in_column(ProjectItems.SEGMENTO)

    def unique_in_column(self, column, dt=None):
        if dt is None:
            return self.dt[column].unique()
        else:
            return dt[column].unique()

    def projects_similarity(self, itens_a, itens_b):
        union_size = np.union1d(itens_a, itens_b).size

        intersction_size = np.intersect1d(itens_a, itens_b,
                                          assume_unique=True).size

        return intersction_size / union_size

    def projects_similarity_min(self, itens_a, itens_b):
        union_size = np.union1d(itens_a, itens_b).size

        intersction_size = np.intersect1d(itens_a, itens_b).size

        size = min(itens_a.size, itens_b.size)
        return intersction_size / size


class Projects:

    PROJECT_ROOT = os.path.abspath(os.path.join(os.pardir, os.pardir))
    DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data', 'raw')

    DATE = 'DtProtocolo'
    AREA = 'Area'
    SEGMENTO = 'Segmento'

    def __init__(self, dt=None):
        self.__set_dt(dt)
        self.__filter_dt()

    def __set_dt(self, dt):
        if dt is not None:
            self.dt = dt
        else:
            self.__init_dt_from_csv()
            pass

    def __init_dt_from_csv(self):
        projetos_csv_name = 'projetos.csv'
        projects_csv = os.path.join(Projects.DATA_FOLDER, projetos_csv_name)

        self.dt = pd.read_csv(projects_csv, low_memory=False)

    def __filter_dt(self):
        assert self.dt is not None

        START_DATE = datetime(day=1, month=1, year=2013)

        date_column = Projects.DATE
        self.dt[date_column] = pd.to_datetime(
            self.dt[date_column], format=Dates.DATE_INPUT_FORMAT)
        self.dt = self.dt[self.dt.loc[:, date_column] >= START_DATE]

    def most_frequent_areas(self):
        assert self.dt is not None

        from collections import Counter

        areas = Counter(self.dt[Projects.AREA].values)
        items = areas.items()
        items = sorted(items, key=itemgetter(1), reverse=True)
        return items

    def most_frequent_segments(self):
        assert self.dt is not None

        from collections import Counter

        segments = Counter(self.dt[Projects.SEGMENTO].values)
        items = segments.items()
        items = sorted(items, key=itemgetter(1), reverse=True)
        return items

    def most_frequent_area_segment(self):
        assert self.dt is not None
        res = self.dt.groupby([Projects.AREA,
                               Projects.SEGMENTO]).size().reset_index(name='Frequency')
        res.sort_values(by='Frequency', ascending=False, inplace=True)
        return res
