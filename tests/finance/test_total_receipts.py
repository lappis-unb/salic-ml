import unittest

from salicml.data.query import metrics

EXPECTED_KEYS = ["is_outlier", "total_receipts", "maximum_expected_in_segment"]


class TestTotalReceipts(unittest.TestCase):
    def test_inlier_pronac(self):
        project = metrics.get_project(152066)
        response = project.finance.total_receipts
        assert all(key in response for key in EXPECTED_KEYS)
        assert not response['is_outlier']

    def test_outlier_pronac(self):
        project = metrics.get_project(1510865)
        response = project.finance.total_receipts
        assert all(key in response for key in EXPECTED_KEYS)
        assert response['is_outlier']
