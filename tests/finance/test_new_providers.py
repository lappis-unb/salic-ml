import unittest


from core.utils.read_csv import read_csv_with_different_type
from core.finance.metrics.new_providers import NewProviders


class TestNewProviders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        csv_name = "planilha_comprovacao.csv"
        usecols = NewProviders.usecols

        super(TestNewProviders, cls).setUpClass()

        cls.dt_comprovacao = read_csv_with_different_type(
            csv_name, {"PRONAC": str, "nrCNPJCPF": str}, usecols=usecols
        )
        cls.new_providers = NewProviders(cls.dt_comprovacao)

    def test_outlier_pronac(self):
        pronac = "153038"

        response = self.new_providers.get_metrics(pronac)
        self.assertTrue(response["is_outlier"])
        self.assertTrue(response["new_providers"])

    def test_inlier_pronac(self):
        pronac = "130222"
        response = self.new_providers.get_metrics(pronac)
        self.assertFalse(response["is_outlier"])

    def test_get_metrics(self):
        pronac = "130222"
        response = self.new_providers.get_metrics(pronac)

        expected_keys = [
            "new_providers",
            "new_providers_percentage",
            "segment_average_percentage",
            "is_outlier",
            "all_projects_average_percentage",
        ]

        for key in expected_keys:
            self.assertIn(key, response.keys())
