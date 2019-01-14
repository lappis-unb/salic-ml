import os

from learning.features.number_of_items import FeatureNumberOfItems
from learning.metrics.number_of_items import NumberOfItemsModel
from learning.middleware.exceptions import TraningNotFound
from learning.middleware import constants


class NumberOfItemsMiddleware:
    """This class is a middleware specialist in the metric NumberOfItems.
    It gets all necessary raw data from DataSource, extracts the feature
    NumberOfItems, and makes inference on that feature"""

    TRAIN_NUMBER_OF_METRICS_PATH = os.path.join(
        constants.TRAIN_FOLDER, "number_of_items.pickle"
    )
    COLUMNS = ["PRONAC", "idSegmento", "idPlanilhaAprovacao"]

    def __init__(self, data_source):
        self._data_source = data_source
        self.number_of_items = NumberOfItemsModel()

    def load_number_of_items(self):
        """Tries to load the training model for the feature"""
        self.number_of_items.load(
            NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH,
            self.on_load_number_of_items_error,
        )

    def on_load_number_of_items_error(self):
        """Callback function on the case of there is no trained stored to be
        loaded"""
        raise TraningNotFound("Number of Items training not found")

    def train_number_of_items(self, planilha_orcamentaria, save=True):
        """Extracts the feature, trains a model on the extracted feature and
        returns the trained model. If save=True, the trained model will also
         be saved as a .picke file"""
        feature = FeatureNumberOfItems()
        items_features = feature.get_projects_number_of_items(planilha_orcamentaria)

        self.number_of_items.train(items_features)

        if save:
            self.number_of_items.save(
                NumberOfItemsMiddleware.TRAIN_NUMBER_OF_METRICS_PATH
            )

    def get_metric_number_of_items(self, pronac):
        """Makes inference and calculate the metric number of items for the
        given pronac. The pronac's data will downloaded from the SALIC database
        so its guaranted to be up-to-date."""
        feature = FeatureNumberOfItems()
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            columns=NumberOfItemsMiddleware.COLUMNS, pronac=pronac
        )
        items_features = feature.get_projects_number_of_items(planilha_orcamentaria)

        _, id_segment, number_of_items = items_features[0]

        result = self.number_of_items.is_outlier(number_of_items, id_segment)
        result["number_of_items"] = number_of_items
        result["minimum_expected"] = 0
        return result
