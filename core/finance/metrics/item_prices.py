from datetime import datetime

import pandas as pd
import numpy as np

from salicml.outliers import gaussian_outlier


class ItemsPrice():
    """ TODO
    """
    usecols = ['PRONAC', 'idPlanilhaAprovacao', 'Item', 'idPlanilhaItens',
               'VlUnitarioAprovado', 'idSegmento', 'DataProjeto']

    def __init__(self, dt_orcamentaria):
        """ TODO
        """
        assert isinstance(dt_orcamentaria, pd.DataFrame)

        self.dt_orcamentaria = dt_orcamentaria[ItemsPrice.usecols].copy()
        self._train()

    def get_metrics(self, pronac):
        """ TODO
        """
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        PERCENTAGE_THRESHOLD = .1
        outliers, total_items, outliers_percentage, items_outlier = \
            self.get_outliers_percentage(pronac)

        outlier = outliers_percentage > PERCENTAGE_THRESHOLD
        response = {
            'is_outlier': outlier,
            'number_items_outliers': outliers,
            'total_items': total_items,
            'maximum_expected': PERCENTAGE_THRESHOLD * total_items,
            'outlier_items': items_outlier,
        }
        return response

    def _train(self):
        """ TODO
        """

        self.dt_train = self.dt_orcamentaria.copy()

        START_DATE = datetime(2013, 1, 1)

        self.dt_train['DataProjeto'] = pd.to_datetime(self.dt_train['DataProjeto'])
        self.dt_train = self.dt_train[self.dt_train.DataProjeto >= START_DATE]
        self.dt_train = self.dt_train[self.dt_train.VlUnitarioAprovado > 0.0]

        PRICE_COLUMNS = ['idSegmento', 'idPlanilhaItens', 'VlUnitarioAprovado']
        self.dt_train_agg = self.dt_train[PRICE_COLUMNS].groupby(
            by=['idSegmento', 'idPlanilhaItens']).agg(
            [np.mean, lambda x: np.std(x, ddof=0)])
        self.dt_train_agg.columns = self.dt_train_agg.columns.droplevel(0)
        self.dt_train_agg.rename(columns={'<lambda>': 'std'}, inplace=True)

        self.pronacs_grp = self.dt_orcamentaria[
            ['PRONAC', 'idPlanilhaItens', 'VlUnitarioAprovado',
             'idSegmento', 'Item', ]].groupby(['PRONAC'])

    def is_item_outlier(self, id_planilha_item, id_segmento, price):
        if (id_segmento, id_planilha_item) not in self.dt_train_agg.index:
            return False

        mean = self.dt_train_agg.loc[(id_segmento, id_planilha_item)]['mean']
        std = self.dt_train_agg.loc[(id_segmento, id_planilha_item)]['std']
        outlier = gaussian_outlier.is_outlier(x=price, mean=mean,
                                              standard_deviation=std)
        return outlier

    def get_outliers_percentage(self, pronac):
        items = self.pronacs_grp.get_group(pronac)

        outliers = 0
        items_outliers = {}

        for row in items.itertuples():
            item_id = getattr(row, 'idPlanilhaItens')
            unit_value = getattr(row, 'VlUnitarioAprovado')
            segment_id = getattr(row, 'idSegmento')
            item_name = getattr(row, 'Item')

            is_outlier = self.is_item_outlier(id_planilha_item=item_id,
                                             id_segmento=segment_id,
                                             price=unit_value)
            if is_outlier:
                outliers += 1
                items_outliers[item_id] = item_name

        outliers_percentage = outliers / items.shape[0]
        return outliers, items.shape[0], outliers_percentage, items_outliers


