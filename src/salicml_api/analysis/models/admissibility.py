from .base import Indicator
from boogie.rest import rest_api


@rest_api(["value"], inline=True)
class AdmissibilityIndicator(Indicator):

    METRICS = {"planilha_orcamentaria": ["common_items_ratio"]}

    class Meta:
        app_label = "analysis"
        proxy = True

    @property
    def metric_weights(self):
        return {"common_items_ratio": 1}
