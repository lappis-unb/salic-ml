import pandas as pd

import salicml.outliers.gaussian_outlier as gaussian_outlier


class VerifiedFunds():
    """Responsable for detecting anomalies in projects total verified funds.
    This class maintains a internal cache of projects data so any information
    need should be present in the dataset passed to the constructor.
    """
    def __init__(self, dt_verified_funds):
        """ All information needed to answer future requests to this class will
        be saved/cached in this function. Saves information about each
        individual project as well as projects in each of the segments.
        """
        assert isinstance(dt_verified_funds, pd.DataFrame)

        self.dt_verified_funds = dt_verified_funds
        self._init_metrics_cache()
        self._init_projects_data()

    def get_metrics(self, pronac):
        """ Calculates whether a given pronac is an anomaly or not in terms of
        it's total verified funds.  Uses the internal cache to get data about
        the given pronac.
        """
        is_outlier, mean, std = self.is_pronac_outlier(pronac)
        total_verified_funds = self.get_pronac_verified_funds(pronac)
        maximum_expected_funds = gaussian_outlier.maximum_expected_value(mean, std)

        response = {
            'is_outlier': is_outlier,
            'total_verified_funds': total_verified_funds,
            'maximum_expected_funds': maximum_expected_funds
        }
        return response

    def _init_metrics_cache(self):
        """ Saves metrics for each segment from the dataset. These metrics will
        be used to calculate whether a given pronac is an anomaly or not.
        """

        segment_projects = self.dt_verified_funds[['PRONAC', 'idSegmento',
        'vlComprovacao']].groupby(['idSegmento', 'PRONAC']).sum()

        segment_funds_avg_std = segment_projects.groupby(['idSegmento'])
        segment_funds_avg_std = segment_funds_avg_std.agg(
            ['count', 'sum', 'mean', 'std'])

        segment_funds_avg_std.columns = \
            segment_funds_avg_std.columns.droplevel(0)

        self._segments_cache = segment_funds_avg_std.to_dict(orient='index')

    def _init_projects_data(self):
        """ Saves data about each individual project from the dataset """
        self._dt_projects = self.dt_verified_funds[['idPlanilhaAprovacao', 'PRONAC', 'vlComprovacao', 'idSegmento']]

        self.project_funds_grp = self._dt_projects.drop(columns=['idPlanilhaAprovacao']).groupby(['PRONAC'])
        self.project_funds = self.project_funds_grp.sum()

    def is_pronac_outlier(self, pronac):
        """ Tests if the given pronac is a gaussian outlier in terms of it's
        total verified funds. It is assumed that the data follows a Gaussian
        distribution """
        verified_funds = self.get_pronac_verified_funds(pronac)
        id_segmento = self.get_pronac_segment(pronac)

        if not id_segmento in self._segments_cache:
            raise ValueError('Segment {} was not trained'.format(id_segmento))

        mean = self._segments_cache[id_segmento]['mean']
        std = self._segments_cache[id_segmento]['std']
        outlier = gaussian_outlier.is_outlier(verified_funds, mean, std)
        return (outlier, mean, std)


    def get_pronac_verified_funds(self, pronac):
        return self.project_funds.loc[pronac]['vlComprovacao']

    def get_pronac_segment(self, pronac):
        return self.project_funds_grp.get_group(pronac).iloc[0]['idSegmento']


