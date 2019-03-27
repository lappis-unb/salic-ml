from boogie.rest import rest_api
from .utils import default_metrics, metrics_name_map


# Project aditional attribute
@rest_api.property('projects.Project')
def complexidade(obj):
    """
    Returns a value that indicates project health, currently FinancialIndicator
    is used as this value, but it can be a result of calculation with other
    indicators in future
    """
    indicators = obj.indicator_set.all()
    if not indicators:
        value = 0.0
    else:
        value = indicators.first().value
    return value


# Metric aditional attributes #
@rest_api.property('projects.Metric')
def project_pronac(obj):
    return obj.indicator.project.pronac


@rest_api.property('projects.Metric')
def detail(obj):
    """
    Returns data as json (since it is a picklefield in database, it has
    serialization issues)
    """
    return obj.data


# Project aditional end point /projects/PRONAC_NUMBER/details
@rest_api.detail_action('projects.Project')
def details(project):
    """
    Project detail endpoint,
    Returns project pronac, name,
    and indicators with details
    """
    indicators = project.indicator_set.all()
    indicators_detail = [(indicator_details(i)
                         for i in indicators)][0]
    if not indicators:
        indicators_detail = [
                        {'FinancialIndicator':
                            {'valor': 0.0,
                             'metrics': default_metrics, }, }]
    indicators_detail = convert_list_into_dict(indicators_detail)

    return {'pronac': project.pronac,
            'nome': project.nome,
            'indicadores': indicators_detail,
            }


def indicator_details(indicator):
    """
    Return a dictionary with all metrics in FinancialIndicator,
    if there aren't values for that Indicator, it is filled with default values
    """
    metrics = format_metrics_json(indicator)

    metrics_list = set(indicator.metrics
                       .filter(name__in=metrics_name_map.keys())
                       .values_list('name', flat=True))
    null_metrics = default_metrics
    for keys in metrics_list:
        null_metrics.pop(metrics_name_map[keys], None)

    metrics.update(null_metrics)

    return {type(indicator).__name__: {
            'valor': indicator.value,
            'metricas': metrics, },
            }


# utils
def convert_list_into_dict(list):
    return dict((key, d[key]) for d in list for key in d)


def format_metrics_json(indicator):
    metrics = [
                {metrics_name_map[m.name]: {
                      'valor': m.value,
                      'data': m.data,
                      'valor_valido': True,
                      'is_outlier': m.is_outlier,
                      'minimo_esperado': m.data.get('minimo_esperado', 0),
                      'maximo_esperado': m.data.get('maximo_esperado', 0)
                  },
                 } for m in indicator
                .metrics.filter(name__in=metrics_name_map.keys())]
    return convert_list_into_dict(metrics)
