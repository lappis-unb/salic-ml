"""
Pre loads measurements from database saved projects
"""
from .models import create_finance_metrics, FinancialIndicator
from salicml.data import data
# ==============================================================================
# AUXILIAR FUNCTIONS


def load_project_metrics():
    """
    Create project metrics for financial indicator
    Updates them if already exists
    """
    all_metrics = FinancialIndicator.METRICS
    for key in all_metrics:
        df = getattr(data, key)
        pronac = 'PRONAC'
        if key == 'planilha_captacao':
            pronac = 'Pronac'
        pronacs = df[pronac].unique().tolist()
        create_finance_metrics(all_metrics[key], pronacs)

    indicators = FinancialIndicator.objects.all()
    for indicator in indicators():
        indicator.calculate_proponent_projects_weight()
