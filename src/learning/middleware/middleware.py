from salicml.data_source.data_source_db import DataSourceDb
from salicml.middleware.number_of_items import NumberOfItemsMiddleware
from salicml.middleware.verified_approved import VerifiedApprovedMiddleware
from salicml.middleware.exceptions import TraningNotFound


class Middleware:
    """This class is responsable for getting raw data from DataSource, calling
    feature extraction processes on that raw data and training or making
    inferences on the extracted features. The training or inference processes
    are expected to be used on an external service, e.g Flask or Django web
    servers or CLI."""

    def __init__(self, data_source=None):
        self._init_data_source(data_source)
        self._init_all_middlewares()

    def _init_data_source(self, data_source):
        self._data_source = data_source if data_source else DataSourceDb()

    def train_all(self, save=True):
        """Trains the models for all implemented feature-middlewares. It will
        try to load the stored training models. If there's no training stored,
        it will train the model and store it if save=True. """
        planilha_orcamentaria = self._get_planilha_orcamentaria()

        self.number_of_items_middleware.train_number_of_items(
            planilha_orcamentaria, save
        )

    def load_all(self):
        """Tries to load the training model from disk. If the training model is
        not found on disk, it will be trained and saved."""
        try:
            self.number_of_items_middleware.load_number_of_items()
        except TraningNotFound:
            planilha_orcamentaria = self._get_planilha_orcamentaria()
            self.number_of_items_middleware.train_number_of_items(
                planilha_orcamentaria, True
            )

    def _init_number_of_items_middleware(self):
        self.number_of_items_middleware = NumberOfItemsMiddleware(self._data_source)

    def get_metric_number_of_items(self, pronac):
        return self.number_of_items_middleware.get_metric_number_of_items(pronac)

    def get_metric_verified_approved(self, pronac):
        return self.verified_approved_middleware.get_metric_verified_approved(pronac)

    def _get_planilha_orcamentaria(self):
        """Singleton implementation of planilha orcamentaria. """
        planilha_orcamentaria = self._data_source.get_planilha_orcamentaria(
            use_cache=True
        )

        return planilha_orcamentaria

    def _init_all_middlewares(self):
        self._init_number_of_items_middleware()
        self._init_verified_approved_middleware()

    def _init_verified_approved_middleware(self):
        self.verified_approved_middleware = VerifiedApprovedMiddleware(
            self._data_source
        )
