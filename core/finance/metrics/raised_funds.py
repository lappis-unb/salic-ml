import os
import numpy as np
import pandas as pd
import salicml.outliers.gaussian_outlier as gaussian_outlier

from core.data_handler.data_source import DataSource

class RaisedFunds():

    def __init__(self, dt_raised_funds):
        """ TODO
        """
        print('*** RaisedFunds ***')
        assert isinstance(dt_raised_funds, pd.DataFrame)
        dt_raised_funds['CaptacaoReal'] = dt_raised_funds['CaptacaoReal'].apply(pd.to_numeric)
        self.dt_raised_funds = dt_raised_funds
        self._init_metrics_cache()
        self._init_projects_data()

    def get_metrics(self, pronac):
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        is_outlier, mean, std, total_raised_funds = self.is_pronac_outlier(pronac)
        maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

        response = {
            'is_outlier': is_outlier,
            'total_raised_funds': total_raised_funds,
            'maximum_expected_funds': maximum_expected_funds
        }
        return response

    def is_pronac_outlier(self, pronac):
        """ TODO
        """

        pronac_data = self._get_pronac_data(pronac)

        if not pronac_data['segment_id'] in self._segments_cache:
            raise ValueError('Segment {} was not trained'.format(pronac_data['segment_id']))

        mean = self._segments_cache[pronac_data['segment_id']]['mean']
        std = self._segments_cache[pronac_data['segment_id']]['std']
        outlier = gaussian_outlier.is_outlier(pronac_data['raised_funds'], mean, std)
        return (outlier, mean, std, pronac_data['raised_funds'])

    def _init_metrics_cache(self):
        """ TODO
        """
        pronac_segment_projects = self.dt_raised_funds[['Pronac', 'Segmento', 'CaptacaoReal']].groupby(
            ['Segmento', 'Pronac']).sum()
        segment_projects = pronac_segment_projects.groupby(['Segmento'])
        segment_funds_avg_std = segment_projects.agg(['count', 'sum', 'mean', 'std'])
        segment_funds_avg_std.columns = segment_funds_avg_std.columns.droplevel(0)
        self._segments_cache = segment_funds_avg_std.to_dict(orient='index')

    def _init_projects_data(self):
        """ TODO
        """
        self._dt_projects = self.dt_raised_funds[['Pronac', 'Segmento', 'CaptacaoReal']]
        self.raised_funds_by_pronac = self._dt_projects.groupby(['Pronac'])

        self.project_funds = self.raised_funds_by_pronac.sum()

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_captacao.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)
        pronac_dataframe['CaptacaoReal'] = pronac_dataframe['CaptacaoReal'].apply(pd.to_numeric)

        pronac_data = {
            'segment_id': pronac_dataframe.iloc[0]['Segmento'],
            'raised_funds': pronac_dataframe[['Pronac', 'CaptacaoReal']].groupby(['Pronac']).sum().loc[pronac]['CaptacaoReal']
        }

        return pronac_data