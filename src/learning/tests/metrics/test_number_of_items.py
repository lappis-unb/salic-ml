import unittest

from learning.metrics.number_of_items import NumberOfItemsModel


class TestMetricNumberOfItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.features = [
            ["000000", "A", 1],
            ["000001", "A", 2],
            ["000002", "A", 3],
            ["000003", "A", 500],
            ["000005", "B", 3],
            ["000006", "B", 2],
            ["000007", "B", 3],
        ]

    def test_train(self):
        items_features = [
            ["000001", "A", 1],
            ["000002", "A", 11],
            ["000003", "B", 2],
            ["000004", "B", 20],
            ["000005", "C", 3],
        ]

        number_of_items = NumberOfItemsModel()
        number_of_items.train(items_features)

        self.assertEqual(3, len(number_of_items.segments_trained))

        self.assertEqual(6, number_of_items.segments_trained["A"]["mean"])
        self.assertEqual(11, number_of_items.segments_trained["B"]["mean"])
        self.assertEqual(3, number_of_items.segments_trained["C"]["mean"])

        self.assertEqual(5, number_of_items.segments_trained["A"]["std"])
        self.assertEqual(9, number_of_items.segments_trained["B"]["std"])
        self.assertEqual(0, number_of_items.segments_trained["C"]["std"])

    def test_inlier_pronac(self):
        number_of_items = 4
        id_segment = "A"

        model = NumberOfItemsModel()
        model.train(self.features)

        inference = model.is_outlier(number_of_items, id_segment)
        is_outlier = inference[NumberOfItemsModel.IS_OUTLIER_KEY]
        max_expected = inference[NumberOfItemsModel.MAX_EXPECTED_KEY]

        self.assertFalse(is_outlier)
        self.assertLessEqual(number_of_items, max_expected)
