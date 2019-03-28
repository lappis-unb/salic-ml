from boogie.rest import rest_api
from polymorphic.managers import PolymorphicManager

from salicml.data.query import metrics as metrics_calc
from .metric import Metric
from .base import Indicator
from .project import Project


class FinancialIndicatorManager(PolymorphicManager):
    def create_indicator(self, project, is_valid, metrics_list):
        """
        Creates FinancialIndicator object for a project, calculating
        metrics and indicator value
        """
        project = Project.objects.get(pronac=project)
        indicator = FinancialIndicator.objects.update_or_create(project=project)[0]
        indicator.is_valid = is_valid
        if indicator.is_valid:
            p_metrics = metrics_calc.get_project(project.pronac)
            for metric_name in metrics_list:
                print("calculando a metrica  ", metric_name)
                x = getattr(p_metrics.finance, metric_name)
                print("do projeto: ", project)
                Metric.objects.create_metric(metric_name, x, indicator)
            indicator.fetch_weighted_complexity()
        return indicator


@rest_api(["value"], inline=True)
class FinancialIndicator(Indicator):
    """
    Rates a project according to financial aspect, using the folowing metrics
        - Items
        - Funds to verify
        - Proponent projects
        - New providers
        - Verified and approved
        - Approved funds
        - Items prices
        - Common items ratio
        - Total receipts
    """

    METRICS = {
        "planilha_aprovacao_comprovacao": ["verified_approved"],
        "planilha_captacao": ["to_verify_funds"],
        "planilha_comprovacao": [
            "proponent_projects",
            "new_providers",
            "total_receipts",
        ],
        "planilha_orcamentaria": ["number_of_items"],
    }

    objects = FinancialIndicatorManager()

    class Meta:
        app_label = "analysis"

    @property
    def metrics_weights(self):
        return {
            "number_of_items": 1,
            "to_verify_funds": 5,
            "proponent_projects": 2,
            "new_providers": 1,
            "verified_approved": 2,
            "verified_funds": 0,
            "common_items_ratio": 0,
            "total_receipts": 0,
            "items_prices": 0,
        }

    def calculate_indicator_metrics(self):
        p_metrics = metrics_calc.get_project(self.project.pronac)
        metrics = FinancialIndicator.METRICS
        for metric_name in metrics:
            for metric in metrics[metric_name]:
                print("calculando a metrica  ", metric)
                x = getattr(p_metrics.finance, metric)
                print("do projeto: ", self.project)
                Metric.objects.create_metric(metric, x, self)

    def __str__(self):
        return self.project.nome + " value: " + str(self.value)
