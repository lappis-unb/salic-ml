"""
Pre loads measurements from database saved projects
"""
import multiprocessing as mp

from django import db

from .models import create_indicators_metrics, Indicator, FinancialIndicator, AdmissibilityIndicator
from salicml.data import data


def load_project_metrics(indicator_class):
    """
    Create project metrics for financial indicator
    Updates them if already exists
    """
    all_metrics = {**indicator_class.METRICS}
    
    #close db connections here
    db.connections.close_all()

    processors = mp.cpu_count()
    print(f"Using {processors} processors to calculate metrics!")
    
    process_list = []

    for planilha in all_metrics:
        
        process = mp.Process(
            target=start_calculation,
            args=(planilha, all_metrics, indicator_class)
        )
        process_list.append(process)
        process.start()

    [p.join() for p in process_list]

    print("Finished metrics calculation!\n")


def start_calculation(planilha, all_metrics, indicator_class):
    df = getattr(data, planilha)
    pronac = 'PRONAC'
    if planilha == 'planilha_captacao':
        pronac = 'Pronac'
    
    pronacs = df[pronac].unique().tolist()
    inner_process_list = []
    for metric in all_metrics[planilha]:
        print(f'Calculating metric "{metric}"\n')
        inner_process = mp.Process(
            target=create_indicators_metrics,
            args=([metric], pronacs, indicator_class)
        )
        inner_process_list.append(inner_process)
        inner_process.start()
        
    [p.join() for p in inner_process_list]