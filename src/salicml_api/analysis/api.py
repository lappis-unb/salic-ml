from boogie.rest import rest_api

from .utils import default_admissibility_metrics, default_financial_metrics, financial_metrics_names
from .models import FinancialIndicator, AdmissibilityIndicator


values_to_order = ['nome', '-nome', 'pronac', '-pronac'
                   'responsavel', '-responsavel']


@rest_api.query_hook('analysis.Project')
def query(request, qs):
    qs = qs.prefetch_related('indicator_set')
    if request.method == 'GET':
        for field, value in request.GET.items():
            if field == 'complexidade__gt':
                qs = qs.filter(indicator__value__gt=value)
            elif field == 'order_by':
                if value == 'complexidade':
                    qs = qs.order_by("indicator__value")
                elif value == '-complexidade':
                    qs = qs.order_by("-indicator__value")
                elif value in values_to_order:
                    qs = qs.order_by(value)
            elif field == 'nome__icontains':
                dictionary = {field: value}
                qs = qs.filter(**dictionary)
            elif field == 'complexidade':
                qs = qs.filter(indicator__value=value)

    return qs


# Project aditional attribute
@rest_api.property('analysis.Project')
def complexidade(obj):
    """
    Returns a value that indicates project health, currently FinancialIndicator
    is used as this value, but it can be a result of calculation with other
    indicators in future
    """
    return obj.complexidade


# Metric aditional attributes #
@rest_api.property('analysis.Metric')
def project_pronac(obj):
    return obj.indicator.project.pronac


@rest_api.property('analysis.Metric')
def detail(obj):
    """
    Returns data as json (since it is a picklefield in database, it has
    serialization issues)
    """
    return obj.data


# Project aditional end point /projects/PRONAC_NUMBER/details
@rest_api.detail_action('analysis.Project')
def details(project):
    """
    Project detail endpoint,
    Returns project pronac, name,
    and indicators with details
    """
    indicators = project.indicator_set.all()
    indicators_detail = [indicator_details(i) for i in indicators]
    if not indicators:
        indicators_detail = [
                        {'FinancialIndicator':
                            {'valor': 0.0,
                             'metrics': default_financial_metrics, }, },

                        {'AdmissibilityIndicator':
                             {'valor': 0.0,
                              'metrics': default_admissibility_metrics, }, },
                        ]
    indicators_detail = convert_list_into_dict(indicators_detail)

    return {'pronac': project.pronac,
            'nome': project.nome,
            'indicadores': indicators_detail,
            }


def indicator_details(indicator):
    """
    Return a dictionary with all metrics in FinancialIndicator and
    AdmissibilityIndicator. If there aren't values for those Indicators,
    they are filled with default values.
    """
    metrics = format_metrics_json(indicator)

    metrics_set = set(indicator.metrics
                       .filter(name__in=financial_metrics_names)
                       .values_list('name', flat=True))
    null_metrics = {}
    if isinstance(indicator, FinancialIndicator):
        null_metrics.update(default_financial_metrics)
    elif isinstance(indicator, AdmissibilityIndicator):
        null_metrics.update(default_admissibility_metrics)

    for metric in metrics_set:
        null_metrics.pop(metric, None)

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
                {m.name: {
                      'valor': m.value,
                      'data': m.data,
                      'valor_valido': True,
                      'is_outlier': m.is_outlier,
                      'minimo_esperado': m.data.get('minimo_esperado', 0),
                      'maximo_esperado': m.data.get('maximo_esperado', 0)
                  },
                 } for m in indicator
                .metrics.filter(name__in=financial_metrics_names)]
    return convert_list_into_dict(metrics)
