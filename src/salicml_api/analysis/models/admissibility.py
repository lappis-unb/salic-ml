from .base import Indicator
from boogie.rest import rest_api


@rest_api(["value"], inline=True)
class AdmissibilityIndicator(Indicator):

    METRICS = {"planilha_orcamentaria": ["itens_comuns_e_incomuns_por_segmento"]}

    class Meta:
        app_label = "analysis"
        proxy = True

    @property
    def metrics_weights(self):
        return {"itens_comuns_e_incomuns_por_segmento": 1}

    def calculate_proponent_projects_weight(self):
        return None