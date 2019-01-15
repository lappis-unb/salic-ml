import unittest

from salicml.data.query import metrics
from salicml.metrics.finance.approved_funds import approved_funds


class TestApprovedFunds(unittest.TestCase):
    def setUp(self):
        metrics.register(approved_funds)

    def test_inlier_pronac(self):
        project = metrics.get_project('138140')
        self.assertFalse(project.finance.approved_funds['is_outlier'])

    def test_outlier_pronac(self):
        project = metrics.get_project('121386')
        self.assertTrue(project.finance.approved_funds['is_outlier'])
