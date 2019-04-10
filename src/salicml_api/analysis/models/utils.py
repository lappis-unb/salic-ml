import logging
from django.db import IntegrityError, transaction
from itertools import product, chain

from salicml.data.db_connector import db_connector
from salicml.data.db_operations import DATA_PATH
from salicml.data.query import metrics as metrics_calc

from . import FinancialIndicator
from . import Metric
from . import Project

log = logging.getLogger("salic-ml.data")
LOG = log.info
MODEL_FILE = DATA_PATH / "scripts" / "models" / "general_project_data.sql"


def execute_project_models_sql_scripts(force_update=False):
    """
        Used to get project information from MinC database
        and convert to this application Project models.
        Uses bulk_create if database is clean
    """
    # TODO: Remove except and use ignore_conflicts
    # on bulk_create when django 2.2. is released
    with open(MODEL_FILE, "r") as file_content:
        query = file_content.read()
        db = db_connector()
        query_result = db.execute_pandas_sql_query(query)
        db.close()
        try:
            projects = Project.objects.bulk_create(
                (Project(**vals) for vals in query_result.to_dict("records")),
                # ignore_conflicts=True available on django 2.2.
            )
            indicators = [FinancialIndicator(project=p) for p in projects]
            FinancialIndicator.objects.bulk_create(indicators)
        except IntegrityError:
            # happens when there are duplicated projects
            LOG("Projects bulk_create failed, creating one by one...")
            with transaction.atomic():
                if force_update:
                    for item in query_result.to_dict("records"):
                        p, _ = Project.objects.update_or_create(**item)
                        FinancialIndicator.objects.update_or_create(project=p)
                else:

                    for item in query_result.to_dict("records"):
                        p, _ = Project.objects.get_or_create(**item)
                        FinancialIndicator.objects.update_or_create(project=p)


def create_finance_metrics(metrics: list, pronacs: list):
    """
    Creates metrics, creating an Indicator if it doesn't already exists
    Metrics are created for projects that are in pronacs and saved in
    database.

        args:
            metrics: list of names of metrics that will be calculated
            pronacs: pronacs in dataset that is used to calculate those metrics
    """

    missing = missing_metrics(metrics, pronacs)
    indicators_qs = FinancialIndicator.objects.filter(project_id__in=[p for _, p in missing])
    indicators = {i.project_id: i for i in indicators_qs}
    metrics = []

    for metric_name, pronac in missing:
        indicator = indicators[pronac]
        p_metrics = metrics_calc.get_project(pronac)
        x = getattr(p_metrics.finance, metric_name)

        metrics.append(Metric.create_metric(name=metric_name,
                                            data=x, indicator=indicator))

    Metric.objects.bulk_create(metrics)

    for indicator in indicators.values():
        indicator.fetch_weighted_complexity_without_proponent_projects()


def missing_metrics(metrics, pronacs):
    projects_metrics = Project.objects.filter(pronac__in=pronacs).values_list(
        "pronac", "indicator__metrics"
    )
    projects_pronacs = [p for p, _ in projects_metrics]

    return set(product(metrics, projects_pronacs)) - set(projects_metrics)
