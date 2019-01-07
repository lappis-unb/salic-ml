import unittest

from core.utils.read_csv import read_csv_with_different_type
from core.finance.metrics.approved_funds import ApprovedFunds


class TestApprovedFunds(unittest.TestCase):
    def setUp(self):
        csv_name = "planilha_orcamentaria.csv"
        usecols = ApprovedFunds.needed_columns

        self.dt_approved_funds = read_csv_with_different_type(
            csv_name, {"PRONAC": str}, usecols=usecols
        )
        self.assertIsNotNone(self.dt_approved_funds)

        self.approved_funds = ApprovedFunds(self.dt_approved_funds)

    def test_init_mean_std(self):
        cache = self.approved_funds._segments_cache
        self.assertTrue(cache)

        mean_std = ["mean", "std"]

        for segment in cache.keys():
            map(lambda x: self.assertIn(x, cache[segment]), mean_std)

    def test_inlier_pronac(self):
        pronac = "138140"

        is_outlier, mean, std = self.approved_funds.is_pronac_outlier(pronac)
        self.assertFalse(is_outlier)

    def test_outlier_pronac(self):
        pronac = "121386"

        is_outlier, mean, std = self.approved_funds.is_pronac_outlier(pronac)
        self.assertTrue(is_outlier)
