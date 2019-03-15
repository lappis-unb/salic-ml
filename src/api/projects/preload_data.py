"""
Pre loads measurements from database saved projects
"""
from projects.models import create_finance_metrics, FinancialIndicator
from salicml.data import data
import pandas as pd
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
        pronacs = pd.to_numeric(df[pronac]).unique().tolist()
        create_finance_metrics(all_metrics[key], pronacs)
