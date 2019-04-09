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
        raise NotImplementedError("implement in subclass")

    def fetch_weighted_complexity(self, recalculate_metrics=False):
        """
        Calculates indicator value according to metrics weights
        Uses metrics in database
        args:
            recalculate_metrics: If true metrics values are updated before
                                 using weights
        """
        # TODO: implment metrics recalculation
        max_total = sum(
            [self.metrics_weights[metric_name] for metric_name in self.metrics_weights]
        )
        total = 0
        if recalculate_metrics:
            self.calculate_indicator_metrics()
        for metric in self.metrics.all():
            if metric.name in self.metrics_weights and metric.is_outlier:
                total += self.metrics_weights[metric.name]

        value = total / max_total

        final_value = "{:.1f}".format(value * 10)

        if final_value[-1] == "0":
            final_value = "{:.0f}".format(value * 10)
            final_value = int(final_value)
        else:
            final_value = float(final_value)
        self.value = float(final_value)
        self.is_valid = True
        self.updated_at = datetime.datetime.now()
        self.save()
        return final_value
