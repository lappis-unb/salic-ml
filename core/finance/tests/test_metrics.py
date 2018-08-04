import unittest

from core.finance.financial_metrics import FinancialMetrics


class TestFinancialMetrics(unittest.TestCase):

    def setUp(self):
        self.fm = FinancialMetrics()

    def test_init(self):
        print('starting fm')
        print('fm loaded')
        print(self.fm.datasets)
        print(self.fm.metrics)
        self.assertTrue(True)

    def test_get_metrics_verified_funds(self):
        key = 'verified_funds'
        pronac = 178098
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)
        self.assertTrue(len(response) == 1)

        response_funds = response[key]
        self.assertIsInstance(response_funds, dict)

        expected_keys = ['is_outlier', 'total_verified_funds',
                         'maximum_expected_funds']
        map(lambda key: self.assertIn(key, response_funds), expected_keys)

