from boogie.rest import rest_api
from .utils import default_metrics
PER_PAGE = 15

metrics_name_map = {
    'number_of_items': 'itens_orcamentarios',
    'to_verify_funds': 'valor_a_ser_comprovado',
    'verified_approved': 'comprovantes_acima_de_50',
    'total_receipts': 'comprovantes_pagamento',
    'approved_funds': 'valor_aprovado', # DEPRECATED
    'common_items_ratio': 'itens_orcamentarios_fora_do_comum', # DEPRECATED
    'item_prices': 'precos_acima_media', # DEPRECATED
    'new_providers': 'novos_fornecedores',
    'proponent_projects': 'projetos_mesmo_proponente',
}

# Project aditional attributes
@rest_api.property('projects.Project')
def indicators(obj):
    return [{'value': i.value,
             'type': type(i).__name__}
            for i in obj.indicator_set.all()]


@rest_api.property('projects.Metric')
def detail(obj):
    return obj.data


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
                        {'valor': 10,
                        'metrics': default_metrics,},}]
    indicators_detail = dict((key,d[key]) for d in indicators_detail for key in d)

    print(indicators_detail)
    return {'pronac': project.pronac,
            'nome': project.name,
            'indicadores': indicators_detail,
            }


def indicator_details(indicator):
    """
    Return a dictionary with all metrics in FinancialIndicator,
    if there aren't values for that Indicator, it is filled with default values
    """
    # LISTA PRA {} DONE
    # métrica valor a ser comprovado
    metrics_list = set(indicator.metrics.all().values_list('name', flat=True))
    null_metrics = default_metrics
    for keys in metrics_list:
        null_metrics.pop(metrics_name_map[keys], None)
    metrics =  [
                {metrics_name_map[m.name]: {
                      'valor': m.value,
                      'data': m.data,
                      'valor_valido': True,
                      'is_outlier': m.is_outlier,
                      'minimo_esperado': m.data.get('minimo_esperado', 0),
                      'maximo_esperado': m.data.get('maximo_esperado', 0)
                  },
                 } for m in indicator.metrics.all()]
    metrics = dict((key,d[key]) for d in metrics for key in d)
    metrics.update(null_metrics)
    return {type(indicator).__name__:{
            'valor': indicator.value,
            'metricas': metrics,},
            }
