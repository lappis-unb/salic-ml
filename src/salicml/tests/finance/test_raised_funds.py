import unittest

from salicml.data.query import metrics


class TestRaisedFunds(unittest.TestCase):

    def test_inlier_pronac(self):
        pronac = "153699"
        project = metrics.get_project(pronac)

        response = project.finance.raised_funds
        assert not response['is_outlier']

    def test_outlier_pronac(self):
        pronac = "178098"
        project = metrics.get_project(pronac)

        response = project.finance.raised_funds
        assert response['is_outlier']
