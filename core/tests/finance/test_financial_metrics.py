import unittest
from core.finance.financial_metrics import FinancialMetrics

class TestFinancialMetrics(unittest.TestCase):

    def setUp(self):
        self.fm = FinancialMetrics()

    def test_init(self):
        print('\n[TEST] Test if the financial metrics are loaded as expected')
        print('datasets: {}'.format(self.fm.datasets.keys()))
        print('metrics: {}'.format(self.fm.metrics.keys()))
        assert True

    def test_num_items(self):
        print('\n[TEST] Test if the metric \'number of items\' is correct')
        pronac = 90105
        metric = 'items'
        print('Getting project #{} results...'.format(pronac))
        results = self.fm.get_metrics(pronac, metrics=[metric])
        print(results)
        assert (results[metric]['is_outlier'] == False)

    def test_get_metrics_verified_funds(self):
        print('\n[TEST] Test if the metric \'total verified funds\' is correct')
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

    def test_get_metrics_raised_funds(self):
        key = 'verified_funds'
        pronac = 178098
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)
        self.assertTrue(len(response) == 1)

        response_funds = response[key]
        self.assertIsInstance(response_funds, dict)

        expected_keys = ['is_outlier', 'total_raised_funds',
                         'maximum_expected_funds']
        map(lambda key: self.assertIn(key, response_funds), expected_keys)

    def test_get_proponent_projects(self):
        pronac = '00000000000000'
        key = 'proponent_projects'
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        response_propoents = response[key]
        self.assertIsInstance(response_propoents, dict)

        expected_keys = ['cnpj_cpf', 'submitted_projects', 'analyzed_projects']
        map(lambda key: self.assertIn(key, response_propoents), expected_keys)

