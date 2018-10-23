import os
import pandas as pd
import numpy as np

from salicml.outliers import gaussian_outlier
from datetime import datetime
from core.data_handler.data_source import DataSource

class ItemsPrice():
    """ TODO
    """
    usecols = ['PRONAC', 'idPlanilhaAprovacao', 'Item', 'idPlanilhaItens',
               'VlUnitarioAprovado', 'idSegmento', 'DataProjeto', 'idPronac',
                'UfItem', 'idProduto', 'cdCidade', 'cdEtapa', ]


    def __init__(self, dt_orcamentaria, dt_comprovacao):
        """ TODO
        """
        assert isinstance(dt_orcamentaria, pd.DataFrame)

        self.dt_orcamentaria = dt_orcamentaria[ItemsPrice.usecols].copy()
        self.dt_orcamentaria['VlUnitarioAprovado'] = self.dt_orcamentaria['VlUnitarioAprovado'].apply(pd.to_numeric)
        self.dt_comprovacao = self._process_receipt_data(dt_comprovacao)
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

        self.pronacs_grp = self.dt_orcamentaria.groupby(['PRONAC'])

    def is_item_outlier(self, id_planilha_item, id_segmento, price):
        if (id_segmento, id_planilha_item) not in self.dt_train_agg.index:
            return False

        mean = self.dt_train_agg.loc[(id_segmento, id_planilha_item)]['mean']
        std = self.dt_train_agg.loc[(id_segmento, id_planilha_item)]['std']
        outlier = gaussian_outlier.is_outlier(x=price, mean=mean,
                                              standard_deviation=std)
        return outlier

    def get_outliers_percentage(self, pronac):
        items = self._get_pronac_data(pronac)

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
                item_salic_url = self._item_salic_url(row)
                has_receipt = self._item_has_receipt(row)
                items_outliers[item_id] = {'name': item_name,
                                           'salic_url': item_salic_url,
                                           'has_receipt': has_receipt}


        outliers_percentage = outliers / items.shape[0]
        return outliers, items.shape[0], outliers_percentage, items_outliers

    def _item_salic_url(self, item_info):
        url_keys = [
            ('pronac', 'idPronac'),
            ('uf', 'uf'),
            ('product', 'produto'),
            ('county', 'idmunicipio'),
            ('item_id', 'idPlanilhaItem'),
            ('stage', 'etapa')
        ]

        url_values = {
            'pronac': getattr(item_info, 'idPronac'),
            'uf': getattr(item_info, 'UfItem'),
            'product': getattr(item_info, 'idProduto'),
            'county': getattr(item_info, 'cdCidade'),
            'item_id': getattr(item_info, 'idPlanilhaItens'),
            'stage': getattr(item_info, 'cdEtapa')
        }

        item_data = []
        for key, value in url_keys:
            item_data.append((value, url_values[key]))

        URL_PREFIX = '/prestacao-contas/analisar/comprovante'
        url = URL_PREFIX
        for key, value in item_data:
            url += '/' + str(key) + '/' + str(value)

        return url


    def _item_has_receipt(self, item_info):
        item_identifier = str(getattr(item_info, 'idPronac')) + '/' + str(getattr(item_info, 'idPlanilhaItens'))
        return item_identifier in self.dt_comprovacao.index


    def _process_receipt_data(self, dt_comprovacao):
        dt_comprovacao = dt_comprovacao[['IdPRONAC', 'idPlanilhaItem']].astype(str)
        dt_comprovacao['pronac_planilha_itens'] = dt_comprovacao['IdPRONAC'] + '/' + dt_comprovacao['idPlanilhaItem']
        dt_comprovacao.set_index(['pronac_planilha_itens'], inplace=True)
        return dt_comprovacao

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_orcamentaria.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)

        pronac_dataframe = pronac_dataframe[ItemsPrice.usecols]

        pronac_grp = pronac_dataframe.groupby(['PRONAC'])

        return pronac_grp.get_group(pronac)