"""
Pre loads measurements from database saved projects
"""
import multiprocessing as mp
from .models import create_indicators_metrics, Indicator, FinancialIndicator, AdmissibilityIndicator
from salicml.data import data


def load_project_metrics(indicator_class):
    """
    Create project metrics for financial indicator
    Updates them if already exists
    """
    all_metrics = {**indicator_class.METRICS}

    processors = mp.cpu_count()
    print(f"Using {processors} processors to calculate metrics!")

    for planilha in all_metrics:
        df = getattr(data, planilha)
        pronac = 'PRONAC'
        if planilha == 'planilha_captacao':
            pronac = 'Pronac'
        pronacs = df[pronac].unique().tolist()

        for metric in all_metrics[planilha]:
            print(f'Calculating metric "{metric}"')
            create_indicators_metrics([metric], pronacs, indicator_class)

    indicators = Indicator.objects.all()
    for indicator in indicators:
        indicator.calculate_proponent_projects_weight()
