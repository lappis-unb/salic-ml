import unittest


from salicml.data.query import metrics
from salicml.metrics.finance import new_providers


class TestNewProviders(unittest.TestCase):

    def test_outlier_pronac(self):
        project = metrics.get_project('153038')

        response = project.finance.new_providers
        assert response['is_outlier']
        assert response['new_providers']

    def test_inlier_pronac(self):
        project = metrics.get_project('130222')
        response = project.finance.new_providers
        assert not (response['is_outlier'])

    def test_get_metrics(self):
        project = metrics.get_project('130222')
        response = project.finance.new_providers

        expected_keys = [
            'new_providers',
            'new_providers_percentage',
            'segment_average_percentage',
            'is_outlier',
            'all_projects_average_percentage',
        ]
        assert all(key in response for key in expected_keys)
