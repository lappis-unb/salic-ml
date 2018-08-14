import pandas as pd
import numpy as np

import salicml.outliers.gaussian_outlier as gaussian_outlier

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
            raise ValueError('No data for PRONAC ({})'.format(pronac))

        total_receipts = self.get_pronac_receipts(pronac)
        id_segmento = self.get_pronac_segment(pronac)

        if not id_segmento in self._segments_cache:
            raise ValueError('Segment {} was not trained'.format(id_segmento))

        mean = self._segments_cache[id_segmento]['mean']
        std = self._segments_cache[id_segmento]['std']
        outlier = gaussian_outlier.is_outlier(total_receipts, mean, std)
        maximum_expected = gaussian_outlier.maximum_expected_value(mean, std)
        return outlier, total_receipts, maximum_expected

    def get_pronac_receipts(self, pronac):
        return self.project_receipts.loc[pronac]['NumeroComprovantes']

    def get_pronac_segment(self, pronac):
        return self.project_receipts_grp.get_group(pronac).iloc[0]['idSegmento']
