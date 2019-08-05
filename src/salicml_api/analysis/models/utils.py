import logging
import multiprocessing as mp
import pandas as pd
import pickle as pkl

from django.db import IntegrityError, transaction
from itertools import product

from salicml.data.db_connector import db_connector
from salicml.data.db_operations import DATA_PATH
from salicml.data.query import metrics as metrics_calc

from . import Indicator, FinancialIndicator, AdmissibilityIndicator
from . import Metric
from . import Project

from salicml.metrics import finance

log = logging.getLogger("salic-ml.data")
LOG = log.info
MODEL_PATH = DATA_PATH / "scripts" / "models"
MODEL_FILE = MODEL_PATH / "general_project_data.sql"
VERIFIED_FUNDS_FILE = MODEL_PATH / "project_valor_comprovado.sql"
RAISED_FUNDS_FILE = MODEL_PATH / "project_valor_captado.sql"

FINANCE = finance

def execute_project_models_sql_scripts(force_update=False, from_file=False):
    """
        Used to get project information from MinC database
        and convert to this application Project models.
        Uses bulk_create if database is clean
    """
    # TODO: Remove except and use ignore_conflicts
    # on bulk_create when django 2.2. is released
    with open(MODEL_FILE, "r") as file_content:
        if from_file:
            print("Using offline file to populate models")
            with open('/data/dump/update_models.pickle', 'rb') as offline_file:
                query_result = pkl.load(offline_file)
        else:
            query = file_content.read()
            db = db_connector()
            query_result = db.execute_pandas_sql_query(query)
            db.close()
            query_result = convert_datetime(query_result)

        # with open('update_models.pickle', 'wb') as offline_file:
        #     pkl.dump(query_result, offline_file, protocol=pkl.HIGHEST_PROTOCOL)
        
        # try:
        projects = Project.objects.bulk_create(
            (Project(**vals) for vals in query_result.to_dict("records")),
            ignore_conflicts=True
        )
        f_indicators = [FinancialIndicator(project=p) for p in projects]
        a_indicators = [AdmissibilityIndicator(project=p) for p in projects]
        FinancialIndicator.objects.bulk_create(f_indicators)
        AdmissibilityIndicator.objects.bulk_create(a_indicators)
        
        create_project_valores(from_file)


def create_project_valores(from_file=False):
    """
        Used to get project information from MinC database,
        valor_comprovado and valor_captado
        and update this information to application Project models.
    """

    if from_file:
        with open('/data/dump/verified_funds_query.pickle', 'rb') as offline_file:
            records = pkl.load(offline_file)
    else:
        records = make_query_to_dict(VERIFIED_FUNDS_FILE)

    # with open('verified_funds_query.pickle', 'wb') as offline_file:
            # pkl.dump(records, offline_file, protocol=pkl.HIGHEST_PROTOCOL)

    with transaction.atomic():
        for value in records:
            (Project.objects
             .filter(pronac=value['pronac'])
             .update(verified_funds=value['valor_comprovado']))

    if from_file:
        with open('/data/dump/raised_funds_query.pickle', 'rb') as offline_file:
            records = pkl.load(offline_file)
    else:
        records = make_query_to_dict(RAISED_FUNDS_FILE)

    # with open('raised_funds_query.pickle', 'wb') as offline_file:
            # pkl.dump(records, offline_file, protocol=pkl.HIGHEST_PROTOCOL)

    with transaction.atomic():
        for value in records:
            (Project.objects
             .filter(pronac=value['pronac'])
             .update(raised_funds=value['valor_captado']))


def create_indicators_metrics(metrics: list, pronacs: list, indicator_class):
    """
    Creates metrics, creating an Indicator if it doesn't already exists
    Metrics are created for projects that are in pronacs and saved in
    database.

        args:
            metrics: list of names of metrics that will be calculated
            pronacs: pronacs in dataset that is used to calculate those metrics
    """
    missing = missing_metrics(metrics, pronacs)
    indicators_qs = indicator_class.objects.filter(
        project_id__in=[p for p, _ in missing]
    )

    print(f"There are {len(missing)} projects missing \"{metrics[0]}\" metric!")

    indicators = {i.project_id: i for i in indicators_qs}

    calculated_metrics = []
    for pronac, metric_name in missing:
        calculated_metrics.append(create_metric(indicators, metric_name, pronac))

    if calculated_metrics:
        Metric.objects.bulk_create(calculated_metrics, batch_size=1000)
        print(f"Bulk \"{metrics[0]}\" metric completed")

        for indicator in indicators.values():
            indicator.fetch_weighted_complexity()

    for indicator in indicators.values():
        indicator.fetch_complexity_without_proponent_projects()
        
    print(f"Finished metric \"{metrics[0]}\" calculation!\n")


def missing_metrics(metrics, pronacs):
    projects_metrics = Project.objects.filter(pronac__in=pronacs).values_list(
        "pronac", "indicator__metrics__name"
    )
    projects_pronacs = [p for p, _ in projects_metrics]
    missing = set(product(projects_pronacs, metrics)) - set(projects_metrics)
    
    return missing


def create_metric(indicators, metric_name, pronac):
    indicator = indicators[pronac]
    p_metrics = metrics_calc.get_project(pronac)
    x = getattr(p_metrics.finance, metric_name)
    
    return Metric.create_metric(name=metric_name, data=x, indicator=indicator)


def convert_datetime(df):
    """
    Adds timezone to valid datetime and converts NaT (pandas) datetime to
    None
    """
    df['start_execution'] = (df['start_execution']
                             .apply(lambda x: x.tz_localize('utc')
                             if not pd.isnull(x) and type(x) != str else x))
    df['end_execution'] = (df['end_execution']
                           .apply(lambda x: x.tz_localize('utc')
                           if not pd.isnull(x) and type(x) != str else x))
    df[['start_execution']] = (df[['start_execution']].astype(object)
                               .where(df[['start_execution']].notnull(), None))
    df[['end_execution']] = (df[['end_execution']].astype(object)
                             .where(df[['end_execution']].notnull(), None))
    return df


def make_query_to_dict(file):
    with open(file, "r") as file_content:
        query = file_content.read()
        db = db_connector()
        query_result = db.execute_pandas_sql_query(query)
        db.close()
        return query_result.to_dict("records")

