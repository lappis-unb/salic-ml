"""
Pre loads measurements from database saved projects
"""
from .models import create_indicators_metrics, Indicator, FinancialIndicator, AdmissibilityIndicator
from salicml.data import data
# ==============================================================================
# AUXILIAR FUNCTIONS


def load_project_metrics():
    """
    Create project metrics for financial indicator
    Updates them if already exists
    """
    all_metrics = {}
    all_metrics.update(FinancialIndicator.METRICS)
    all_metrics.update(AdmissibilityIndicator.METRICS)

    for key in all_metrics:
        df = getattr(data, key)
        pronac = 'PRONAC'
        if key == 'planilha_captacao':
            pronac = 'Pronac'
        pronacs = df[pronac].unique().tolist()
        create_indicators_metrics(all_metrics[key], pronacs)

    indicators = Indicator.objects.all()
    for indicator in indicators:
        indicator.calculate_proponent_projects_weight()
