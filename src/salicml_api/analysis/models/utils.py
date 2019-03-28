import logging
from django.db import IntegrityError, transaction

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
            Project.objects.bulk_create(
                (Project(**vals) for vals in query_result.to_dict("records")),
                # ignore_conflicts=True available on django 2.2.
            )
        except IntegrityError:
            # happens when there are duplicated projects
            LOG("Projects bulk_create failed, creating one by one...")
            with transaction.atomic():
                if force_update:
                    for item in query_result.to_dict("records"):
                        Project.objects.update_or_create(**item)
                else:
                    for item in query_result.to_dict("records"):
                        Project.objects.get_or_create(**item)


def create_finance_metrics(metrics, pronacs_planilha):
    """
    Creates metrics, creating an Indicator if it doesn't already exists
    Metrics are created for projects that are in pronacs_planilha and saved in
    database.
    args:
            metrics: list of names of metrics that will be calculated
            pronacs_planilha: pronacs in dataset that is used to calculate
            those metrics
    """
    project_list = Project.objects.all().values_list("pronac", flat=True)
    intersection = set(project_list).intersection(pronacs_planilha)
    p_metrics = None
    for metric_name in metrics:
        for project in intersection:
            project = Project.objects.get(pronac=project)
            indicator = FinancialIndicator.objects.update_or_create(project=project)[0]
            metric = Metric.objects.filter(name=metric_name, indicator=indicator)

            if not metric.exists():
                p_metrics = metrics_calc.get_project(project.pronac)
                x = getattr(p_metrics.finance, metric_name)
                Metric.objects.create_metric(metric_name, x, indicator)
                indicator.fetch_weighted_complexity()
                indicator.is_valid = True
            else:
                LOG("metric already exists: ", metric)
    return len(intersection)
