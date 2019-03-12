import unittest

from salicml.data.query import metrics

EXPECTED_KEYS = ["is_outlier", "value", "mean", "std"]


class TestNumberOfItems(unittest.TestCase):
    def test_inlier_pronac(self):
        project = metrics.get_project(90105)
        response = project.finance.number_of_items
        assert all(key in response for key in EXPECTED_KEYS)
        assert not response['is_outlier']
