from boogie.rest import rest_api
from .models import Project


# Project aditional attributes
@rest_api.property(Project)
def indicators(obj):
    return [{'value': i.value,
             'metrics': [{'name': m.name, 'value': m.value,
                          'reason': m.reason} for m in i.metrics.all()]}
            for i in obj.indicator_set.all()]
