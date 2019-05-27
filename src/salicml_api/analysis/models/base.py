import datetime

from django.db import models
from polymorphic.models import PolymorphicModel

from .project import Project


class Indicator(PolymorphicModel):
    """
    Rates a project according to one aspect, using weighted metrics to do so
    """

    value = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_valid = models.BooleanField(default=False)

    class Meta:
        app_label = "analysis"

    @property
    def metric_weights(self, **kwargs):
        raise NotImplementedError("metric_weights implement in subclass")

    @property
    def max_total(self, **kwargs):
        raise NotImplementedError("max_total implement in subclass")

    def fetch_weighted_complexity(self, recalculate_metrics=False):
        """
        Calculates indicator value according to metrics weights
        Uses metrics in database
        args:
            recalculate_metrics: If true metrics values are updated before
                                 using weights
        """
        # TODO: implement metrics recalculation
        self.calculate_weighted_complexity(self.metrics_weights,
                                                         recalculate_metrics)

    def calculate_weighted_complexity(self, metrics_weights,
                                      recalculate_metrics=False):
        # TODO: implement metrics recalculation
        if recalculate_metrics:
            self.calculate_indicator_metrics()

        total = 0
        for metric in self.metrics.all():
            if ((metric.name in metrics_weights)
                and metric.is_outlier):
                total += metrics_weights[metric.name]

        value = total / self.max_total

        self.value = float("{:.1f}".format(value * 10))

        self.is_valid = True
        self.updated_at = datetime.datetime.now()
        self.save()
