"""
Pre loads measurements from database saved projects
"""
from salicml.data.query import metrics as metrics_calc
from api_projects.models import Project, FinancialIndicator, Metric
from salicml.metrics.finance import approved_funds

# ==============================================================================
# AUXILIAR FUNCTIONS


def load_project_metrics(project, update=False):
    """
    Create project metrics for financial indicator
    """
    # TODO:If update is True, update project metrics if already exists
    indicator = FinancialIndicator.objects.create_indicator(project=project)
    return indicator


def test_load_project_metrics():
    project = Project.objects.get(pronac='90105')
    p_metrics = metrics_calc.get_project(project.pronac)
    indicator = FinancialIndicator.objects.create(project=project)
    name = 'approved_funds'
    print(p_metrics.finance.approved_funds)
    x = getattr(p_metrics.finance, name)
    a = Metric.create(name, x, indicator)
    print(a)
