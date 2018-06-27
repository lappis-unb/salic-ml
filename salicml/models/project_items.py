import pandas as pd
import numpy as np
from salicml.utils.utils import debug


class ProjectItems:

    ID_PRONAC = 'idPronac'
    ID_ITEM = 'idPlanilhaItens'
    ITEM = 'Item'
    AREA = 'Area'
    SEGMENTO = 'Segmento'


    def __init__(self, data):
        self.dt = data

    def get_rows_by_column_value(self, column, value, dt = None):
        if dt is None:
            return self.dt[self.dt[column] == value]
        else:
            return dt[dt[column] == value]

    def items(self, id_pronac, dt = None):
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

    def unique_in_column(self, column, dt = None):
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

        intersction_size = np.intersect1d(itens_a, itens_b,
        assume_unique=True).size

        size = min(itens_a.size, itens_b.size)
        return intersction_size / size
