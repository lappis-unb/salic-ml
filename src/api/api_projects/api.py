from boogie.rest import rest_api
from .models import Project


# Project aditional attributes
@rest_api.property(Project)
def indicators(obj):
    return [{'value': i.value,
             'type': type(i).__name__,
             'metrics': [{'name': m.name, 'data': m.data,
                          'reason': m.reason} for m in i.metrics.all()]}
            for i in obj.indicator_set.all()]
