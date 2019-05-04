from boogie.rest import rest_api
from django.db import models
from picklefield import PickledObjectField

from .base import Indicator


@rest_api(["is_outlier", "name"])
class Metric(models.Model):
    indicator = models.ForeignKey(
        Indicator, on_delete=models.CASCADE, related_name="metrics"
    )
    is_outlier = models.BooleanField(default=False)
    data = PickledObjectField(null=True)
    name = models.CharField(max_length=200, default="Metric")
    value = models.CharField(max_length=200, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "analysis"
        unique_together = (("name", "indicator"),)

    def __str__(self):
        return (
            self.name
            + " "
            + str(self.indicator.project.pronac)
            + " "
            + str(self.is_outlier)
        )

    def create_metric(name, data, indicator):
        """
        Creates Metric object for an Indicator
        """
        value = 0
        if "is_outlier" in data:
            is_outlier = data["is_outlier"]
            del data["is_outlier"]
        else:
            is_outlier = False
        if "valor" in data:
            value = data["valor"]
            del data["valor"]
        metric = Metric(
            name=name,
            is_outlier=is_outlier,
            indicator=indicator,
            value=value,
            data=data,
        )
        return metric
