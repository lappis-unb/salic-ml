from salicml.metrics.finance.financial_metrics import FinancialMetrics
from salicml.utils.get_project_info_from_pronac import GetProjectInfoFromPronac
from .models import Entity

# Instanciating FinancialMetrics global module
financial_metrics = FinancialMetrics()

# Uncomment line below when deploying
financial_metrics.save()

# Financial metrics module project list
submitted_projects_info = GetProjectInfoFromPronac()

# Financial complexity pre fetching
pre_fetched_indicators = {}


def load_fetched_indicators():
    for project in Entity.objects.all():
        try:
            pre_fetched_indicators["{0}".format(project.pronac)] = project.indicators.get(
                name='complexidade_financeira').value
        except:
            continue


try:
    load_fetched_indicators()
except:
    pass


def fetch_project_complexity(pronac):
    try:
        indicator_value = pre_fetched_indicators["{0}".format(pronac)]
    except:
        indicator_value = 10

    return indicator_value
