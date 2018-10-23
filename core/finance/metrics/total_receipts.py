import os
import pandas as pd
import numpy as np
import salicml.outliers.gaussian_outlier as gaussian_outlier

from core.data_handler.data_source import DataSource
from core.utils.exceptions import DataNotFoundForPronac

class TotalReceipts():
    usecols = ['PRONAC', 'idSegmento', 'idComprovantePagamento']

    def __init__(self, dt_comprovacao):
        """
            TODO.
        """
        print('*** TotalReceipts ***')
        assert isinstance(dt_comprovacao, pd.DataFrame)

        self.dt_total_receipts = dt_comprovacao[TotalReceipts.usecols].copy()
        self._init_metrics_cache()
        self._init_projects_data()

    def get_metrics(self, pronac):
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        is_outlier, total_receipts, maximum_expected = \
            self.is_pronac_outlier(pronac)

        response = {
            'is_outlier': is_outlier,
            'total_receipts': total_receipts,
            'maximum_expected_in_segment': maximum_expected,
        }

        return response

    def _init_metrics_cache(self):
        segment_projects = \
            self.dt_total_receipts.groupby(['idSegmento', 'PRONAC']).nunique()

        segment_projects_std = segment_projects['idComprovantePagamento']. \
            groupby(['idSegmento']).agg([np.mean, lambda x: np.std(x, ddof=0)])

        segment_projects_std.rename(columns={'<lambda>': 'std'}, inplace=True)

        self._segments_cache = segment_projects_std.to_dict(orient='index')

    def _init_projects_data(self):
        self.project_receipts_grp = self.dt_total_receipts.groupby(['PRONAC'])
        self.project_receipts = self.project_receipts_grp.nunique()

        self.project_receipts.drop(
            columns=['PRONAC', 'idSegmento'],
            inplace=True,
        )

        self.project_receipts.rename(
            columns={'idComprovantePagamento': 'NumeroComprovantes'},
            inplace=True,
        )

    def is_pronac_outlier(self, pronac):
        if not pronac in self.dt_total_receipts.PRONAC.unique():
            raise DataNotFoundForPronac('TotalReceipts')

        pronac_data = self._get_pronac_data(pronac)

        if not pronac_data['segment_id'] in self._segments_cache:
            raise ValueError('Segment {} was not trained'.format(pronac_data['segment_id']))

        mean = self._segments_cache[pronac_data['segment_id']]['mean']
        std = self._segments_cache[pronac_data['segment_id']]['std']
        outlier = gaussian_outlier.is_outlier(pronac_data['total_receipts'], mean, std)
        maximum_expected = gaussian_outlier.maximum_expected_value(mean, std)
        return outlier, pronac_data['total_receipts'], maximum_expected

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_comprovacao.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)

        pronac_data = {
            'segment_id': pronac_dataframe.iloc[0]['idSegmento'],
            'total_receipts': pronac_dataframe.shape[0]
        }

        return pronac_data