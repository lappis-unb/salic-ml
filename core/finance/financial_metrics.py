from core.utils.read_csv import read_csv
from core.finance.metrics.number_of_items import NumberOfItems
from core.finance.metrics.verified_funds import VerifiedFunds


class FinancialMetrics():
    def __init__(self):
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
            'verified_funds': VerifiedFunds(self.datasets['comprovacao'])
        }
