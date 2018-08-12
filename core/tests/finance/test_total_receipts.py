import unittest


from core.utils.read_csv import read_csv
from core.finance.metrics.total_receipts import TotalReceipts

class TestTotalReceipts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        csv_name = 'planilha_comprovacao.csv'
        usecols = TotalReceipts.usecols


        super(TestTotalReceipts, cls).setUpClass()

        cls.dt_comprovacao = read_csv(csv_name, usecols=usecols)
        cls.total_receipts = TotalReceipts(cls.dt_comprovacao)

    def test_outlier_pronac(self):
        pronac = '1510865'

        response = self.total_receipts.get_metrics(pronac)
        self.assertTrue(response['is_outlier'])

        total_receipts = response['total_receipts']
        maximum_expected_in_segment = response['maximum_expected_in_segment']

        self.assertTrue(total_receipts > maximum_expected_in_segment)

    def test_inlier_pronac(self):
        pronac = '152066'

        response = self.total_receipts.get_metrics(pronac)
        self.assertFalse(response['is_outlier'])

        total_receipts = response['total_receipts']
        maximum_expected_in_segment = response['maximum_expected_in_segment']

        self.assertTrue(total_receipts <= maximum_expected_in_segment)

    def test_get_metrics(self):
        pronac = '152066'
        response = self.total_receipts.get_metrics(pronac)

        expected_keys = ['is_outlier', 'total_receipts',
            'maximum_expected_in_segment', ]

        for key in expected_keys:
            self.assertIn(key, response.keys())
