import requests
import os

BASE_URL = os.environ.get('LAPPIS_LEARNING_URL', 'https://lappislearning.lappis.rocks')


class HttpFinancialMetrics:
    def __init__(self, base_url):
        self.base_url = base_url

    def request_json(self, endpoint):
        response = requests.get(self.base_url + endpoint)
        json = response.json()
        return json

    def number_of_items(self, pronac):
        endpoint = "/metric/number_of_items/{0}".format(pronac)
        response = self.request_json(endpoint)
        return response

    def verified_approved(self, pronac):
        endpoint = "/metric/verified_approved/{0}".format(pronac)
        response = self.request_json(endpoint)
        return response

    def fetch_metric(self, metric_name, pronac):
        metric_names = {
            'verified_approved': self.verified_approved,
            'number_of_items': self.number_of_items
        }

        return metric_names[metric_name](pronac)


http_financial_metrics_instance = HttpFinancialMetrics(BASE_URL)
