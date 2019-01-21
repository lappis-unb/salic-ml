import unittest

from salicml.data.query import metrics
from salicml.metrics.finance import approved_funds

class TestApprovedFunds(unittest.TestCase):

    def test_inlier_pronac(self):
        project = metrics.get_project('138140')
        assert not project.finance.approved_funds['is_outlier']

    def test_outlier_pronac(self):
        project = metrics.get_project('121386')
        assert project.finance.approved_funds['is_outlier'] 
