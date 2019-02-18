from boogie.rest import rest_api
PER_PAGE = 15


# Project aditional attributes
@rest_api.property('api_projects.Project')
def indicators(obj):
    return [{'value': i.value,
             'type': type(i).__name__}
            for i in obj.indicator_set.all()]


@rest_api.property('api_projects.Metric')
def detail(obj):
    return obj.data


@rest_api.detail_action('api_projects.Project')
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
    return {'nome': type(indicator).__name__,
            'valor': indicator.value,
            'metricas': [{'name': m.name, 'data': m.data,
                         'outlier': m.is_outlier
                          } for m in indicator.metrics.all()]
            }
