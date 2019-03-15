from boogie.rest import rest_api
PER_PAGE = 15

metrics_name_map = {
    'number_of_items': 'itens_orcamentarios',
    'raised_funds': 'valor_captado',
    'approved_funds': 'valor_aprovado', # DEPRECATED
    'common_items_ratio': 'itens_orcamentarios_fora_do_comum',
    'total_receipts': 'comprovantes_pagamento',
    'new_providers': 'novos_fornecedores',
    'proponent_projects': 'projetos_mesmo_proponente',
    'item_prices': 'precos_acima_media',
    'verified_approved': 'comprovantes_acima_de_50',
    'to_verify_funds': 'valor_a_ser_comprovado',
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
    List of authors.
    """
    return {'pronac': project.pronac,
            'nome': project.name,
            'indicadores': [(indicator_details(i)
                            for i in project.indicator_set.all())]
            }


def indicator_details(indicator):
    # LISTA PRA {}
    # SRC/UTILS/METRICS.JS
    # VALOR valido: para todas as métricas, se  tiver false é pq não existe
    # a métrica
    # minimo esperado: quando não existir passar zero
    # valores de todas as métricas: máximo, mínimo, valor_valido
    # métrica valor a ser comprovado
    # metricas melhor não ser uma lista, tem que ser algo mais fácil de acessar
    return {'nome': type(indicator).__name__,
            'valor': indicator.value,
            'metricas': [{metrics_name_map[m.name]: {
                              'valor': m.value,
                              'data': m.data,
                              'valor_valido': True,
                              'is_outlier': m.is_outlier,
                              'minimo_esperado': data.get('minimo_esperado', 0),
                              'maximo_esperado': data.get('maximo_esperado', 0)
                          }
                          } for m in indicator.metrics.all()]
            }
