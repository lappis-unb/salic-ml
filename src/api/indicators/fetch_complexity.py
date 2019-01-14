from .views import projects_to_analyse, register_project_indicator
from .models import Entity, Metric, Indicator
from .financial_metrics_instance import financial_metrics
from .utils import indicators_average


def get_financial_complexity(metrics):
    try:
        value = indicators_average.fetch_weighted_complexity(metrics)
    except:
        value = 10

    return value


def pre_fetch_financial_complexity():
    try:
        projects = projects_to_analyse(None)
    except:
        projects = []

    for project in projects:
        try:
            entity = Entity.objects.get(pronac=int(project['pronac']))
        except:
            entity = Entity.objects.create(pronac=int(
                project['pronac']), name=project['nome'])

        metrics = financial_metrics.get_metrics(project['pronac'])
        print("Complexity value:", get_financial_complexity(metrics))
        financial_complexity_indicator = register_project_indicator(int(
            project['pronac']), 'complexidade_financeira', get_financial_complexity(metrics))
