import os
import pickle

from core.utils.read_csv import read_csv, PROJECT_ROOT
from core.finance.metrics.number_of_items import NumberOfItems
from core.finance.metrics.verified_funds import VerifiedFunds
from core.finance.metrics.raised_funds import RaisedFunds


class FinancialMetrics():
    PROCESSED_FILE_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed',
                                    'financial_metrics.pickle')

    def __init__(self):
        self.load()

    def initialize(self):
        self._init_datasets()
        self._init_metrics()

    def get_metrics(self, pronac, metrics=[]):
        results = {}

        if metrics is []:
            metrics = self.metrics.keys()

        for metric in metrics:
            if metric in self.metrics:
                results[metric] = self.metrics[metric].get_metrics(pronac)
            else:
                raise Exception('metricNotFound: {}'.format(metric))

        return results

    def _init_datasets(self):
        self.datasets = {
            'orcamento': read_csv('planilha_orcamentaria.csv'),
            'comprovacao': read_csv('planilha_comprovacao.csv'),
            'captacao': read_csv('planilha_captacao.csv')
        }

    def _init_metrics(self):
        self.metrics = {
            'items': NumberOfItems(self.datasets['orcamento']),
            'verified_funds': VerifiedFunds(self.datasets['comprovacao']),
            'raised_funds': RaisedFunds(self.datasets['captacao'])
        }

    def save(self):
        with open(FinancialMetrics.PROCESSED_FILE_PATH, 'wb') as ofile:
            pickle.dump(self, ofile, pickle.HIGHEST_PROTOCOL)

    def load(self):
        if os.path.isfile(FinancialMetrics.PROCESSED_FILE_PATH):
            with open(FinancialMetrics.PROCESSED_FILE_PATH, 'rb') as ifile:
                financial_metrics = pickle.load(ifile)
                self.__dict__.update(financial_metrics.__dict__)
        else:
            self.initialize()
