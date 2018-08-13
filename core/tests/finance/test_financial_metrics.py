import unittest
from core.finance.financial_metrics import FinancialMetrics


class TestFinancialMetrics(unittest.TestCase):
    fm = FinancialMetrics()

    @classmethod
    def setUpClass(cls):
        super(TestFinancialMetrics, cls).setUpClass()

        cls.fm = TestFinancialMetrics.fm

    def test_init(self):
        print('\n[TEST] Test if the financial metrics are loaded as expected')
        print('datasets: {}'.format(self.fm.datasets.keys()))
        print('metrics: {}'.format(self.fm.metrics.keys()))
        assert True

    def test_get_metrics_num_items(self):
        print('\n[TEST] Test if the metric [number of items] is correct')
        pronac = 90105
        metric = 'items'
        print('Getting project #{} results...'.format(pronac))
        results = self.fm.get_metrics(pronac, metrics=[metric])
        print(results)
        assert (not results[metric]['is_outlier'])

    def test_get_metrics_verified_funds(self):
        print('\n[TEST] Test if the metric [total verified funds] is correct')
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

    def test_get_metrics_common_items_ratio(self):
        print('\n[TEST] Test if the metric [common items ratio] is correct')
        pronac = 90105
        metric = 'common_items_ratio'
        print('Getting project #{} results...'.format(pronac))
        results = self.fm.get_metrics(pronac, metrics=[metric])
        print(results)
        assert (not results[metric]['is_outlier'])

    def test_get_metrics_total_receipts(self):
        key = 'total_receipts'
        pronac = '131886'
        metrics = [key]
        
        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)
        self.assertTrue(len(response) == 1)
        
        response_receipts = response[key]
        self.assertIsInstance(response_receipts, dict)

        expected_keys = ['is_outlier', 'total_receipts',
            'maximum_expected_in_segment', ]

        map(lambda key: self.assertIn(key, response_receipts), expected_keys)

  def test_new_providers(self):
        key = 'new_providers'
        metrics = [key]
        pronac = '130222'

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)
        self.assertTrue(len(response) == 1)

        response_new_providers = response[key]
        self.assertIsInstance(response_new_providers, dict)

        expected_keys = ['new_providers', 'new_providers_percentage',
                 'segment_average_percentage', 'is_outlier',
                 'all_projects_average_percentage', ]

        map(lambda key: self.assertIn(key, response_new_providers),
                        expected_keys)
