from boogie.rest import rest_api
from polymorphic.managers import PolymorphicManager
import numpy

from salicml.data.query import metrics as metrics_calc
from salicml.outliers.gaussian_outlier import is_outlier
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
        indicator, _ = (FinancialIndicator
                        .objects.update_or_create(project=project))
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
        "planilha_comprovacao": [
            "check_receipts",
            "transfer_receipts",
            "money_receipts",
            "proponent_projects",
            "new_providers",
            "total_receipts",
        ],
        "planilha_aprovacao_comprovacao": ["verified_approved"],
        "planilha_captacao": ["to_verify_funds"],
        "planilha_orcamentaria": ["number_of_items"],
    }

    objects = FinancialIndicatorManager()

    class Meta:
        app_label = "analysis"
        proxy = True

    @property
    def metrics_weights(self):
        return {
            "number_of_items": 1,
            "to_verify_funds": 5,
            "proponent_projects": 2,
            "new_providers": 1,
            "verified_approved": 2,
            "transfer_receipts": 5,
            "money_receipts": 5,
            "check_receipts": 1,
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
                Metric.create_metric(metric, x, self)

    def fetch_complexity_without_proponent_projects(self):
        metrics_weights = self.metrics_weights
        del metrics_weights["proponent_projects"]
        return self.calculate_weighted_complexity(metrics_weights)

    def calculate_proponent_projects_weight(self):
        metric = self.metrics.filter(name="proponent_projects").first()
        if metric:
            if isinstance(metric.data["projetos_submetidos"], dict):
                pronacs = (metric.data["projetos_submetidos"]
                           ["pronacs_of_this_proponent"])
                metric.data["projetos_submetidos"] = []
                indicators = (FinancialIndicator.objects
                              .filter(project__pronac__in=pronacs))
                values_list = []
                for indicator in indicators:
                    val = (indicator
                           .fetch_complexity_without_proponent_projects())
                    values_list.append(val)
                    (metric.data["projetos_submetidos"]
                     .append(indicator.get_project_info()))
                std = numpy.std(values_list)
                mean = numpy.mean(values_list)
                value = self.fetch_complexity_without_proponent_projects()
                outlier = is_outlier(value, mean, std)
                metric.is_outlier = outlier
                metric.save()
        return None

    def get_project_info(self):
        start_execution = self.project.start_execution
        end_execution = self.project.end_execution
        return {
            "complexidade": self.value,
            "pronac": self.project.pronac,
            "nome": self.project.nome,
            "periodo_de_execucao": f'{start_execution} a {end_execution}',
            "valor_comprovado": self.project.verified_funds,
            "valor_captado": self.project.raised_funds,
            "situacao": self.project.situation,
        }

    def __str__(self):
        return self.project.nome + " value: " + str(self.value)
