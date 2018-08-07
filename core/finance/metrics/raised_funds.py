import numpy as np
import pandas as pd

import salicml.outliers.gaussian_outlier as gaussian_outlier


class RaisedFunds():

    def __init__(self, dt_raised_funds):
        assert isinstance(dt_raised_funds, pd.DataFrame)
        self.dt_raised_funds = dt_raised_funds

        # self._segments_cache
        self._init_metrics_cache()

        # self.project_funds
        # self.self.raised_funds_by_pronac
        self._init_projects_data()

    def get_metrics(self, pronac):
        is_outlier, mean, std = self.is_pronac_outlier(pronac)
        total_verified_funds = self.get_pronac_verified_funds(pronac)
        maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

        response = {
            'is_outlier': is_outlier,
            'total_verified_funds': total_verified_funds,
            'maximum_expected_funds': maximum_expected_funds
        }
        return response

    def is_pronac_outlier(self, pronac):
        verified_funds = self.get_pronac_verified_funds(pronac)
        id_segmento = self.get_pronac_segment(pronac)

        if not id_segmento in self._segments_cache:
            raise ValueError('Segment {} was not trained'.format(id_segmento))

        mean = self._segments_cache[id_segmento]['mean']
        std = self._segments_cache[id_segmento]['std']
        outlier = gaussian_outlier.is_outlier(verified_funds, mean, std)
        return (outlier, mean, std)

    def _init_metrics_cache(self):
        pronac_segment_projects = self.dt_raised_funds[['Pronac', 'Segmento', 'CaptacaoReal']].groupby(
            ['Segmento', 'Pronac']).sum()
        segment_projects = pronac_segment_projects.groupby(['Segmento'])
        segment_funds_avg_std = segment_projects.agg(
            ['count', 'sum', 'mean', 'std'])
        segment_funds_avg_std.columns = \
            segment_funds_avg_std.columns.droplevel(0)
        self._segments_cache = segment_funds_avg_std.to_dict(orient='index')

    def _init_projects_data(self):
        self._dt_projects = self.dt_raised_funds[['Pronac', 'Segmento', 'CaptacaoReal']]
        self.raised_funds_by_pronac = self._dt_projects.groupby(['Pronac'])

        self.project_funds = self.raised_funds_by_pronac.sum()

    def get_pronac_verified_funds(self, pronac):
        return self.project_funds.loc[pronac]['CaptacaoReal']

    def get_pronac_segment(self, pronac):
        return self.raised_funds_by_pronac.get_group(pronac).iloc[0]['Segmento']

