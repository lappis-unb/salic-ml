import os
import pickle

from core.utils.read_csv import read_csv, read_csv_with_different_type, PROJECT_ROOT
from core.finance.metrics.number_of_items import NumberOfItems
from core.finance.metrics.verified_funds import VerifiedFunds
from core.finance.metrics.raised_funds import RaisedFunds
from core.finance.metrics.common_items_ratio import CommonItemsRatio
from core.finance.metrics.proponent_projects import ProponentProjects
from core.finance.metrics.total_receipts import TotalReceipts
from core.finance.metrics.new_providers import NewProviders
from core.finance.metrics.approved_funds import ApprovedFunds
from core.finance.metrics.item_prices import ItemsPrice
from core.utils.exceptions import DataNotFoundForPronac


class FinancialMetrics():
    PROCESSED_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed',
                                       'financial_metrics.pickle')

    def __init__(self):
        self.load()

    def initialize(self):
        print('****** Obtaining datasets ******')
        self._init_datasets()

        print('****** Computing Metrics ******')
        self._init_metrics()

    def get_metrics(self, pronac, metrics=None):
        if not isinstance(pronac, str):
            raise ValueError('PRONAC type must be str')

        results = {}

        if metrics is None:
            metrics = self.metrics.keys()

        for metric in metrics:
            if metric not in self.metrics:
                raise Exception('metricNotFound: {}'.format(metric))

        for metric in metrics:
            try:
                print('Getting Metrics for [{}]'.format(metric))
                metric_obj = self.metrics[metric]
                results[metric] = metric_obj.get_metrics(pronac)
            except DataNotFoundForPronac as ex:
                print('No data for pronac={} for metric={}, skipping it.'.
                      format(pronac, metric))

        self._add_easiness_to_metrics(results)
        return results

    def _add_easiness_to_metrics(self, metrics):
        """ Add an easiness metric to the dict-like metrics parameter.
            This function modifies the parameter only if easiness is not empty.
        """

        easiness = self.calculate_easiness(metrics)
        if easiness:
            EASINESS_KEY = 'easiness'
            metrics[EASINESS_KEY] = easiness

    def calculate_easiness(self, metrics):
        """ Calculates how easy it should be to analyse the project's finances.
        """
        if not isinstance(metrics, dict):
            raise ValueError('Argument metrics must be dict-like')

        IS_OUTLIER_KEY = 'is_outlier'
        total_metrics = 0
        total_metrics_outliers = 0

        for metric_key, metric in metrics.items():
            if IS_OUTLIER_KEY in metric:
                total_metrics += 1
                total_metrics_outliers += 1 if metric[IS_OUTLIER_KEY] \
                                            else 0

        easiness = {}
        if total_metrics > 0:
            easiness = {
                'easiness': 1 - total_metrics_outliers / total_metrics,
                'total_metrics': total_metrics,
                'total_metrics_outliers': total_metrics_outliers,
            }
        return easiness

    def _init_datasets(self):
        from core.data_handler.data_source import DataSource

        __FILE__FOLDER = os.path.dirname(os.path.realpath(__file__))
        sql_folder = os.path.join(__FILE__FOLDER, os.pardir, os.pardir)
        sql_folder = os.path.join(sql_folder, 'data', 'scripts')

        datasource = DataSource()

        dataset_sql_map = {
            'orcamento': 'planilha_orcamentaria.sql',
            'comprovacao': 'planilha_comprovacao.sql',
            'captacao': 'planilha_captacao.sql',
            'projetos': 'planilha_projetos.sql',
        }

        # TODO: adjust columns types, e.g. PRONAC should be read as a string
        self.datasets = {
            'orcamento': datasource.get_dataset(os.path.join(sql_folder, dataset_sql_map['orcamento']), use_cache=True),
            'comprovacao': datasource.get_dataset(os.path.join(sql_folder, dataset_sql_map['comprovacao']), use_cache=True),
            'captacao': datasource.get_dataset(os.path.join(sql_folder, dataset_sql_map['captacao']), use_cache=True),
            'projetos': datasource.get_dataset(os.path.join(sql_folder, dataset_sql_map['projetos']), use_cache=True),
        }

    def _init_metrics(self):
        self.metrics = {
             'items': NumberOfItems(self.datasets['orcamento'].copy()),
             'approved_funds': ApprovedFunds(self.datasets['orcamento'].copy()),
             'verified_funds': VerifiedFunds(self.datasets['comprovacao'].copy()),
             'raised_funds': RaisedFunds(self.datasets['captacao'].copy()),
             'common_items_ratio': CommonItemsRatio(self.datasets['orcamento'].copy(), self.datasets['comprovacao'].copy()),
             'total_receipts': TotalReceipts(self.datasets['comprovacao'].copy()),
             'new_providers': NewProviders(self.datasets['comprovacao'].copy()),
             'proponent_projects': ProponentProjects(self.datasets['comprovacao'].copy(), \
                                                    self.datasets['projetos'].copy()),
             'items_prices': ItemsPrice(self.datasets['orcamento'].copy(),
                                       self.datasets[
                                           'comprovacao'].copy()),
        }

    def save(self):
        with open(FinancialMetrics.PROCESSED_FILE_PATH, 'wb') as ofile:
            pickle.dump(self, ofile, pickle.HIGHEST_PROTOCOL)

    def load(self):
        is_loaded = self._load_pickle_file()

        if not is_loaded:
            self.initialize()

    def _load_pickle_file(self):
        if not os.path.isfile(FinancialMetrics.PROCESSED_FILE_PATH):
            return False

        try:
            with open(FinancialMetrics.PROCESSED_FILE_PATH, 'rb') as ifile:
                financial_metrics = pickle.load(ifile)
                self.__dict__.update(financial_metrics.__dict__)

            return True

        except:
            os.remove(FinancialMetrics.PROCESSED_FILE_PATH)

            print("Error on read picke file")

            return False
