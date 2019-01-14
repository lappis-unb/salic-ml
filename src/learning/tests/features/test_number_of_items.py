import unittest

from learning.features.number_of_items import FeatureNumberOfItems


class TestFeatureNumberOfItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.projects_items = [
            ["012345", 123, "2A"],
            ["012345", 124, "2A"],
            ["012345", 125, "2A"],
            ["012348", 126, "3A"],
            ["012348", 127, "3A"],
        ]

        cls.pronac_items = [
            ["012345", 123, "2A"],
            ["012345", 124, "2A"],
            ["012345", 125, "2A"],
        ]

    def test_get_one_pronac_number_of_items(self):
        feature = FeatureNumberOfItems()
        number_of_items = feature.get_pronac_number_of_items(self.pronac_items)
        self.assertEqual(len(number_of_items), 3)
        self.assertEqual(number_of_items[2], 3)

    def test_get_pronacs_number_of_items(self):
        feature = FeatureNumberOfItems()
        pronacs_features = feature.get_projects_number_of_items(self.projects_items)

        self.assertEqual(len(pronacs_features), 2)

        expected_result = [["012345", "2A", 3], ["012348", "3A", 2]]
        self.assertEqual(pronacs_features, expected_result)
