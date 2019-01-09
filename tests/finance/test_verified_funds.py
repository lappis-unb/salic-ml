import unittest

from salicml.utils.read_csv import read_csv_with_different_type
from salicml.metrics.finance.verified_funds import VerifiedFunds


class TestVerifiedFunds(unittest.TestCase):
    def setUp(self):
        csv_name = "planilha_comprovacao.csv"
        usecols = ["idPlanilhaAprovacao", "PRONAC", "vlComprovacao", "idSegmento"]

        self.dt_verified_funds = read_csv_with_different_type(
            csv_name, {"PRONAC": str}, usecols=usecols
        )
        self.verified_funds = VerifiedFunds(self.dt_verified_funds)

    def test_IO(self):
        csv_name = "planilha_comprovacao.csv"
        usecols = ["idPlanilhaAprovacao", "PRONAC", "vlComprovacao", "idSegmento"]

        csv = read_csv_with_different_type(csv_name, {"PRONAC": str}, usecols=usecols)
        self.assertIsNotNone(csv)

    def test_init_mean_std(self):
        cache = self.verified_funds._segments_cache
        self.assertTrue(cache)

        mean_std = ["mean", "std"]

        for segment in cache.keys():
            map(lambda x: self.assertIn(x, cache[segment]), mean_std)

    def test_inlier_pronac(self):
        pronac = "153699"

        is_outlier, mean, std = self.verified_funds.is_pronac_outlier(pronac)
        self.assertFalse(is_outlier)

    def test_outlier_pronac(self):
        pronac = "178098"

        is_outlier, mean, std = self.verified_funds.is_pronac_outlier(pronac)
        self.assertTrue(is_outlier)
