import pandas as pd
import numpy as np

import salicml.outliers.gaussian_outlier as gaussian_outlier


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
        is_outlier, mean, std = self.is_pronac_outlier(pronac)
        total_approved_funds = self.get_pronac_total_approved_funds(pronac)
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
        assert isinstance(pronac, int)

        total_approved = self.get_pronac_total_approved_value(pronac)
        id_segmento = self.get_pronac_segment(pronac)

        if not (id_segmento in self._segments_cache):
            raise ValueError('Segment {} was not trained'.format(id_segmento))

        mean = self._segments_cache[id_segmento]['mean']
        std = self._segments_cache[id_segmento]['std']
        outlier = gaussian_outlier.is_outlier(total_approved, mean, std)

        return outlier, mean, std

    def get_pronac_total_approved_value(self, pronac):
        total_approved = self.project_approved.loc[pronac]['VlTotalAprovado']
        return total_approved

    def get_pronac_segment(self, pronac):
        id_segmento = self.project_approved_grp.get_group(pronac). \
            iloc[0]['idSegmento']
        return id_segmento
