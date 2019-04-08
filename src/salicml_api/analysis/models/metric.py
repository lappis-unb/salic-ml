from boogie.rest import rest_api
from django.db import models
from picklefield import PickledObjectField

from .base import Indicator


class MetricManager(models.Manager):
    def create_metric(self, name, data, indicator):
        """
        Creates Metric object for an Indicator
        """
        if "is_outlier" in data:
            is_outlier = data["is_outlier"]
            del data["is_outlier"]
        else:
            is_outlier = None
        if "valor" in data:
            value = data["valor"]
            del data["valor"]
        metric = Metric.objects.update_or_create(
            name=name,
            is_outlier=is_outlier,
            indicator=indicator,
            value=value,
            data=data,
        )
        return metric


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

    objects = MetricManager()

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
