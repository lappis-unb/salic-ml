import pandas as pd



class ProjectItems:

    ID_PRONAC = 'idPronac'
    ID_ITEM = 'idPlanilhaItens'
    ITEM = 'Item'


    def __init__(self, data):
        self.dt = data

    def get_rows_by_column_value(self, column, value):
        return self.dt[self.dt[column] == value]

    def items(self, id_pronac):
        data = self.get_rows_by_column_value(ProjectItems.ID_PRONAC,
                id_pronac)
        return data[ProjectItems.ITEM].values
