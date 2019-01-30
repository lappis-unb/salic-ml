import unittest

from salicml.data.query import metrics
from salicml.metrics.finance import item_prices


class TestApprovedFunds(unittest.TestCase):

    def test_inlier_pronac(self):
        project = metrics.get_project(137225)
        assert not project.finance.item_prices['is_outlier']

    def test_outlier_pronac(self):
        project = metrics.get_project(120991)
        assert project.finance.item_prices['is_outlier'] 

    def test_get_metrics(self):
        project = metrics.get_project(137225)
        response = project.finance.item_prices

        expected_keys = [
            'is_outlier',
            'outliers_amount',
            'total_items',
            'maximum_expected',
            'percentage'
        ]

        for key in expected_keys:
            self.assertIn(key, response.keys())
