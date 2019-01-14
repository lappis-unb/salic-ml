import unittest

from learning.features.verified_approved import VerifiedApprovedFeature

NEEDED_COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]

DATASET = [
    NEEDED_COLUMNS,
    ["123456", "Coca cola", 100, 120],
    ["123456", "Coca cola", 100, 200],
    ["123456", "Coca cola zero", 100, 70],
    ["123456", "Coca cola zero", 100, 100],
    ["123457", "Mouse", 100, 50],
    ["123458", "Teclado", 10, 3],
]


class TestFeatureVerifiedApproved(unittest.TestCase):
    def test_pronac_verified_vs_approved_features(self):
        feature = VerifiedApprovedFeature()
        verified_approved = feature.get_features(DATASET)

        for index, row in verified_approved.iterrows():
            approved_value = row["vlAprovado"]
            verified_value = row["vlComprovacao"]
            self.assertTrue(verified_value > (approved_value * 1.5))
