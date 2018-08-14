import unittest
from core.finance.financial_metrics import FinancialMetrics


class TestFinancialMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestFinancialMetrics, cls).setUpClass()

        cls.fm = FinancialMetrics()

    def test_init(self):
        print('\n[TEST] Test if the financial metrics are loaded as expected')
        print('datasets: {}'.format(self.fm.datasets.keys()))
        print('metrics: {}'.format(self.fm.metrics.keys()))
        assert True

    def test_get_metrics_num_items(self):
        print('\n[TEST] Test if the metric [number of items] is correct')
        pronac = '090105'
        metric = 'items'
        print('Getting project #{} results...'.format(pronac))
        results = self.fm.get_metrics(pronac, metrics=[metric])
        print(results)
        assert (not results[metric]['is_outlier'])

    def test_get_metrics_verified_funds(self):
        print('\n[TEST] Test if the metric [total verified funds] is correct')
        key = 'verified_funds'
        pronac = '178098'
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)

        response_funds = response[key]
        self.assertIsInstance(response_funds, dict)

        expected_keys = ['is_outlier', 'total_verified_funds',
                         'maximum_expected_funds']
        map(lambda key: self.assertIn(key, response_funds), expected_keys)

    def test_get_metrics_raised_funds(self):
        key = 'raised_funds'
        pronac = '178098'
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)

        response_funds = response[key]
        self.assertIsInstance(response_funds, dict)

        expected_keys = ['is_outlier', 'total_raised_funds',
                         'maximum_expected_funds']
        map(lambda key: self.assertIn(key, response_funds), expected_keys)

    def test_get_metrics_common_items_ratio(self):
        print('\n[TEST] Test if the metric [common items ratio] is correct')
        pronac = '090105'
        metric = 'common_items_ratio'
        print('Getting project #{} results...'.format(pronac))
        results = self.fm.get_metrics(pronac, metrics=[metric])
        print(results)
        assert (not results[metric]['is_outlier'])

    def test_get_proponent_projects(self):
        pronac = '178098'
        key = 'proponent_projects'
        metrics = [key]

        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)
        print('Getting project #{} proponent information...'.format(pronac))
        print(response)
        response_propoents = response[key]
        self.assertIsInstance(response_propoents, dict)

        expected_keys = ['cnpj_cpf', 'submitted_projects', 'analyzed_projects']
        map(lambda key: self.assertIn(key, response_propoents), expected_keys)

    def test_get_metrics_total_receipts(self):
        key = 'total_receipts'
        pronac = '131886'
        metrics = [key]
        
        response = self.fm.get_metrics(pronac=pronac, metrics=metrics)

        self.assertIsInstance(response, dict)
        self.assertIn(key, response)

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

        response_new_providers = response[key]
        self.assertIsInstance(response_new_providers, dict)

        expected_keys = ['new_providers', 'new_providers_percentage',
                 'segment_average_percentage', 'is_outlier',
                 'all_projects_average_percentage', ]

        map(lambda key: self.assertIn(key, response_new_providers),
                        expected_keys)

    def test_calculate_easiness_keys(self):
        pronac = '130222'
        metric_names = ['new_providers', 'total_receipts', ]
        metrics = self.fm.get_metrics(pronac=pronac, metrics=metric_names)

        EASINESS_KEY = 'easiness'
        EXPECTED_KEYS = ['easiness', 'total_metrics', 'total_metrics_outliers']

        self.assertIn(EASINESS_KEY, metrics)
        filter(lambda x: self.assertIn(x, metrics[EASINESS_KEY]),
               EXPECTED_KEYS)

    def test_calculate_easiness(self):
        pronac = '130222'
        metric_names = ['new_providers', 'total_receipts', ]
        metrics = self.fm.get_metrics(pronac=pronac, metrics=metric_names)

        EASINESS_KEY = 'easiness'

        easiness = metrics[EASINESS_KEY]
        expected_easiness = {
            'easiness': 1.0,
            'total_metrics': 2,
            'total_metrics_outliers': 0,
        }
        self.assertEqual(easiness, expected_easiness)
