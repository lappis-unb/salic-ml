import unittest


from core.utils.read_csv import read_csv_with_different_type
from core.finance.metrics.item_prices import ItemsPrice

class TestItemsPrice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        csv_name = 'planilha_orcamentaria.csv'
        usecols = ItemsPrice.usecols
        super(TestItemsPrice, cls).setUpClass()

        cls.dt_orcamentaria = read_csv_with_different_type(csv_name, {'PRONAC': str}, usecols=usecols)
        cls.items_price = ItemsPrice(cls.dt_orcamentaria)

    def test_inlier_pronac(self):
        pronac = '137225'
        response = self.items_price.get_metrics(pronac)
        print('response = {}'.format(response))
        self.assertFalse(response['is_outlier'])

    def test_outlier_pronac(self):
        pronac = '120991'
        response = self.items_price.get_metrics(pronac)
        self.assertTrue(response['is_outlier'])

    def test_get_metrics(self):
        pronac = '137225'
        response = self.items_price.get_metrics(pronac)

        expected_keys = ['is_outlier', 'number_items_outliers', 'total_items',
            'maximum_expected', ]

        for key in expected_keys:
            self.assertIn(key, response.keys())


