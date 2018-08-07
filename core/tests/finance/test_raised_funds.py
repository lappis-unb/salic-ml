import unittest

from core.utils.read_csv import read_csv
from core.finance.metrics.raised_funds import RaisedFunds

class TestRaisedFunds(unittest.TestCase):

    def setUp(self):
        csv_name = 'planilha_captacao.csv'
        usecols = ['Pronac', 'Segmento', 'CaptacaoReal']

        self.dt_raised_funds = read_csv(csv_name, usecols=usecols)

        self.raised_funds = RaisedFunds(self.dt_raised_funds)

    def test_IO(self):
        csv_name = 'planilha_captacao.csv'
        usecols = ['Pronac', 'Segmento', 'CaptacaoReal']

        csv = read_csv(csv_name, usecols=usecols)
        self.assertIsNotNone(csv)

    def test_init_mean_std(self):
        cache = self.raised_funds._segments_cache
        self.assertTrue(cache)

        mean_std = ['mean', 'std']

        for segment in cache.keys():
            map(lambda x: self.assertIn(x, cache[segment]), mean_std)

    def test_inlier_pronac(self):
        pronac = 153699

        is_outlier, mean, std = self.raised_funds.is_pronac_outlier(pronac)
        self.assertFalse(is_outlier)

    def test_outlier_pronac(self):
        pronac = 178098

        is_outlier, mean, std = self.raised_funds.is_pronac_outlier(pronac)
        self.assertTrue(is_outlier)