import numpy as np
import pandas as pd

from learning.models import gaussian_outlier
from learning.utils import storage


class NumberOfItemsModel:
    """Trains a model and makes inferences on that model about the number of
    items from SALIC projects"""

    MEAN_KEY = "mean"
    STD_KEY = "std"

    IS_OUTLIER_KEY = "is_outlier"
    MAX_EXPECTED_KEY = "maximum_expected"

    def __init__(self):
        self.segments_trained = None

    def train(self, items_features):
        """Receives features of SALIC projects in a matrix form. The matrix
        must be a python list of python lists, where each inner list represents
        a row in the matrix.

        Matrix format:
        The order of the elements of the inner list must be:
        pronac (str), id_segmento (str), number_of_items (int)

        Example:

        [['012345', '1A', 123],
         ['012346', '2B', 124],
         ['012347', 'A8', 123],
         ['012348', '2A', 123],
         ['012349', '2A', 123], ]
        """

        COLUMNS = ["PRONAC", "id_segmento", "number_of_items"]
        items_df = pd.DataFrame(items_features, columns=COLUMNS)

        self.segments_trained = dict()

        segments_groups = items_df.groupby(["id_segmento"])
        for segment, segment_group in segments_groups:
            number_of_items_array = segment_group.number_of_items.values
            segment_trained = self._train_segment(number_of_items_array)

            self.segments_trained[segment] = segment_trained

    def is_outlier(self, number_of_items, id_segment):
        """Returns wheter the given number of items is an outlier for the given
        segment. """
        assert self.segments_trained is not None

        segment_mean = self.segments_trained[id_segment][NumberOfItemsModel.MEAN_KEY]
        segment_std = self.segments_trained[id_segment][NumberOfItemsModel.STD_KEY]

        outlier = gaussian_outlier.is_outlier(
            number_of_items, segment_mean, segment_std
        )

        maximum_expected = gaussian_outlier.maximum_expected_value(
            segment_mean, segment_std
        )

        result = {
            NumberOfItemsModel.IS_OUTLIER_KEY: outlier,
            NumberOfItemsModel.MAX_EXPECTED_KEY: maximum_expected,
        }
        return result

    def save(self, file_path):
        storage.save(file_path, self.segments_trained)

    def load(self, file_path, on_error_callback=None):
        segments_trained = storage.load(file_path, on_error_callback)

        if segments_trained:
            self.segments_trained = segments_trained

    def _train_segment(self, segment_features):
        """Sets the mean and standard deviation from an array of features
        (number_of_items) and returns it as a dictionary"""

        mean = np.mean(segment_features)
        std = np.std(segment_features)

        result = {NumberOfItemsModel.MEAN_KEY: mean, NumberOfItemsModel.STD_KEY: std}
        return result
