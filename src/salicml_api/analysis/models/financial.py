from boogie.rest import rest_api
from functools import lru_cache
from polymorphic.managers import PolymorphicManager
import numpy

from salicml.data.query import metrics as metrics_calc
from salicml.outliers.gaussian_outlier import is_outlier
from salicml_api.analysis import situations
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
        indicator, _ = (
            FinancialIndicator.objects.update_or_create(project=project))
        indicator.is_valid = is_valid
        if indicator.is_valid:
            project_metrics = metrics_calc.get_project(project.pronac)
            for metric_name in metrics_list:
                x = getattr(project_metrics.finance, metric_name)
                Metric.objects.create_metric(metric_name, x, indicator)
            indicator.fetch_weighted_complexity()

        project.complexity = indicator.value
        project.save()
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
            "comprovante_cheque",
            "comprovante_transferencia",
            "comprovante_saque",
            "novos_fornecedores",
            "comprovante_pagamento",
            "comprovantes_acima_50",
        ],
        "planilha_projetos": ["projetos_mesmo_proponente"],
        "planilha_captacao": ["valor_a_ser_comprovado"],
        "planilha_orcamentaria": ["itens_orcamentarios"],
    }

    objects = FinancialIndicatorManager()

    class Meta:
        app_label = "analysis"
        proxy = True

    @property
    def metrics_weights(self):
        return {
            "itens_orcamentarios": 1,
            "valor_a_ser_comprovado": 5,
            "projetos_mesmo_proponente": 2,
            "novos_fornecedores": 1,
            "comprovantes_acima_50": 2,
            "comprovante_transferencia": 5,
            "comprovante_saque": 5,
            "comprovante_cheque": 1,
            "valor_comprovado": 0,
            "itens_comuns_e_incomuns_por_segmento": 0,
            "comprovante_pagamento": 0,
            "items_prices": 0
        }

    @property
    @lru_cache(maxsize=256)
    def max_weight_total(self):
        return sum(self.metrics_weights.values())

    def calculate_indicator_metrics(self):
        project_metrics = metrics_calc.get_project(self.project.pronac)
        metrics = FinancialIndicator.METRICS
        for metric_name in metrics:
            for metric in metrics[metric_name]:
                x = getattr(project_metrics.finance, metric)
                Metric.create_metric(metric, x, self)

    def fetch_complexity_without_proponent_projects(self):
        new_metrics_weights = self.metrics_weights
        del new_metrics_weights["projetos_mesmo_proponente"]
        return self.calculate_weighted_complexity(new_metrics_weights)

    def calculate_proponent_projects_weight(self):
        metric = self.metrics.filter(name="projetos_mesmo_proponente").first()

        if metric:
            if isinstance(metric.data["projetos_submetidos"], list):
                pronacs = (
                    # metric.data["projetos_submetidos"]["pronacs_of_this_proponent"] # Before uncommenting, check finance/projetos_mesmo_proponente.py
                    metric.data["projetos_submetidos"]
                )
                metric.data["projetos_submetidos"] = []
                indicators = (FinancialIndicator.objects.filter(
                    project__pronac__in=pronacs))
                values_list = []
                for indicator in indicators:
                    val = (
                        indicator.fetch_complexity_without_proponent_projects()
                    )

                    values_list.append(val)
                    (metric.data["projetos_submetidos"]
                     .append(indicator.get_project_info()))

                std = numpy.std(values_list)
                mean = numpy.mean(values_list)
                value = self.fetch_complexity_without_proponent_projects()

                metric.data["valor"] = len(metric.data["projetos_submetidos"])

                outlier = is_outlier(value, mean, std)
                metric.is_outlier = outlier
                metric.save()
        return None

    def get_project_info(self):
        start_execution = self.project.start_execution
        end_execution = self.project.end_execution
        situation_code = self.project.situation

        return {
            "complexidade": self.value,
            "pronac": self.project.pronac,
            "nome": self.project.nome,
            "data_inicio": start_execution,
            "data_final": end_execution,
            "valor_comprovado": self.project.verified_funds,
            "valor_captado": self.project.raised_funds,
            "situacao": situation_code + " - " +
            situations.SITUATIONS_DICT[situation_code],
        }

    def save(self, *args, **kwargs):
        project = self.project
        project.complexity = self.value
        project.save()
        super(Indicator, self).save(*args, **kwargs)


    def __str__(self):
        return self.project.nome + " value: " + str(self.value)
