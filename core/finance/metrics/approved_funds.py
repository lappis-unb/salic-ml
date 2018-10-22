import os
import pandas as pd
import numpy as np
import salicml.outliers.gaussian_outlier as gaussian_outlier

from core.data_handler.data_source import DataSource


class ApprovedFunds():
    """Responsable for detecting anomalies in projects total approved values.
    This class maintains a internal cache of projects data so any information
    need should be present in the dataset passed to the constructor.
    """

    needed_columns = ['PRONAC', 'idSegmento', 'VlTotalAprovado']

    def __init__(self, dt_approved_funds):
        """All information needed to answer future requests to this class will
        be saved/cached in this function.
        """
        print('*** ApprovedFunds ***')
        assert isinstance(dt_approved_funds, pd.DataFrame)

        self.dt_approved_funds = \
            dt_approved_funds[ApprovedFunds.needed_columns]

        self._init_metrics_cache()
        self._init_projects_data()

    def get_metrics(self, pronac):
        """ Calculates whether a given pronac is an anomaly or not in terms of
        it's total approved value.  Uses the internal cache to get data about
        the given pronac.
        """
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        is_outlier, mean, std, total_approved_funds = self.is_pronac_outlier(pronac)
        maximum_expected_funds = \
            gaussian_outlier.maximum_expected_value(mean, std)

        response = {
            'is_outlier': is_outlier,
            'total_approved_funds': total_approved_funds,
            'maximum_expected_funds': maximum_expected_funds
        }
        return response

    def _init_metrics_cache(self):
        """ Saves metrics for each segment from the dataset. These metrics will
        be used to calculate whether a given pronac is an anomaly or not.
        """
        segment_projects = self.dt_approved_funds. \
            groupby(['idSegmento', 'PRONAC']).sum()

        segment_approved_avg_std = segment_projects.groupby(['idSegmento'])
        segment_approved_avg_std = segment_approved_avg_std.agg(
            ['mean', 'std'])

        segment_approved_avg_std.columns = \
            segment_approved_avg_std.columns.droplevel( 0)

        self._segments_cache = segment_approved_avg_std.to_dict(orient='index')

    def _init_projects_data(self):
        """ Saves data about each individual project from the dataset """
        self.project_approved_grp = self.dt_approved_funds.groupby(['PRONAC'])
        self.project_approved = self.project_approved_grp.sum()

    def is_pronac_outlier(self, pronac):
        """ Tests if the given pronac is a gaussian outlier in terms of it's
        total approved value. It is assumed that the data follows a Gaussian
        distribution """
        assert isinstance(pronac, str)

        pronac_data = self._get_pronac_data(pronac)

        if not (pronac_data['segment_id'] in self._segments_cache):
            raise ValueError('Segment {} was not trained'.format(pronac_data['segment_id']))

        mean = self._segments_cache[pronac_data['segment_id']]['mean']
        std = self._segments_cache[pronac_data['segment_id']]['std']
        outlier = gaussian_outlier.is_outlier(pronac_data['approved_funds'], mean, std)

        return outlier, mean, std, pronac_data['approved_funds']

    def _get_pronac_data(self, pronac):
        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()
        path = os.path.join(sql_folder, 'planilha_orcamentaria.sql')

        pronac_dataframe = datasource.get_dataset(path, pronac=pronac)
        pronac_dataframe = pronac_dataframe[ApprovedFunds.needed_columns]

        approved_grp = pronac_dataframe.groupby(['PRONAC'])
        approved = approved_grp.sum()

        pronac_data = {
            'segment_id': pronac_dataframe.iloc[0]['idSegmento'],
            'approved_funds': approved.loc[pronac]['VlTotalAprovado']
        }

        return pronac_data
