import os

from salicml.middleware import constants
from salicml.features.verified_approved import VerifiedApprovedFeature


TRAIN_FILE_NAME = "verified_approved.pickle"
TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(constants.TRAIN_FOLDER, TRAIN_FILE_NAME)
ITEM_NAME_COLUMN = "Item"
MIN_EXPECTED_ITEMS = 0
MAX_EXPECTED_ITEMS = 0


class VerifiedApprovedMiddleware:
    """This class is a middleware specialist in the metric
    Verified vs Approved metric. It gets all necessary raw data from
    DataSource, extracts the feature related features, and makes inference on
    set of features"""

    def __init__(self, data_source):
        self._data_source = data_source

    def get_metric_verified_approved(self, pronac):
        """Makes inference and calculate the metric number of items for the
        given pronac. The pronac's data will downloaded from the SALIC database
        so its guaranted to be up-to-date."""
        feature = VerifiedApprovedFeature()

        planilha_aprovacao_comprovacao_pronac = self._data_source.get_planilha_aprovacao_comprovacao(
            pronac=pronac
        )
        pronac_features = feature.get_features(planilha_aprovacao_comprovacao_pronac)

        result = self.prepare_json(pronac_features)
        return result

    def prepare_json(self, features):
        features_size = features.shape[0]
        is_outlier = features_size > 0
        result = {
            "is_outlier": is_outlier,
            "number_of_outliers": features_size,
            "minimum_expected": MIN_EXPECTED_ITEMS,
            "maximum_expected": MAX_EXPECTED_ITEMS,
        }

        outlier_items = []

        for row in features.itertuples():
            item_name = getattr(row, "Item")
            approved_value = getattr(row, "vlAprovado")
            verified_value = getattr(row, "vlComprovacao")

            item = {
                "item": item_name,
                "approved_value": approved_value,
                "verified_value": verified_value,
            }
            outlier_items.append(item)
        result["outlier_items"] = outlier_items
        return result
