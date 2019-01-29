from django.db import models
from boogie.rest import rest_api
from polymorphic.models import PolymorphicModel
from .projects import Project


class Indicator(PolymorphicModel):
    """
    Rates a project according to one aspect, using weighted metrics to do so
    """
    value = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='indicator_set')

    @property
    def metric_weights(self, **kwargs):
            raise NotImplementedError('implement in subclass')

    def fetch_weighted_complexity(self, metrics):
        max_total = sum([self.metrics_weights[metric_name] for metric_name in
                         self.metrics_weights])
        total = 0
        for metric_name in self.metrics_weights:
            try:
                if metrics[metric_name] is not None:
                    if metrics[metric_name]['is_outlier']:
                        total += self.metrics_weights[metric_name]
            except KeyError:
                pass

        value = total/max_total
        value = 1 - value

        final_value = "{:.1f}".format(value * 10)

        if final_value[-1] == '0':
            final_value = "{:.0f}".format(value * 10)
            final_value = int(final_value)
        else:
            final_value = float(final_value)

        return final_value


@rest_api(['value'], inline=True)
class FinancialIndicator(Indicator):
    """
    Rates a project according to financial aspect, using the folowing metrics
        - Items
        - Funds to verify
        - Proponent projects
        - New providers
        - Verified and approved
        - Approved funds
        - Items prices
        - Common items ratio
        - Total receipts
    """

    @property
    def metrics_weights(self):
        return {
            'items': 1,
            'to_verify_funds': 5,
            'proponent_projects': 2,
            'new_provders': 1,
            'verified_approved': 2,
            'raised_funds': 0,
            'verified_funds': 0,
            'approved_funds': 0,
            'common_items_ratio': 0,
            'total_receipts': 0,
            'items_prices': 0
        }

    def __str__(self):
        return self.project.name + " value: " + str(self.value)


class Metric(models.Model):
    indicator = models.ForeignKey(
        Indicator,
        on_delete=models.CASCADE,
        related_name='metrics')
    value = models.FloatField(default=0.0)
    name = models.CharField(max_length=200, default='Metric')
    reason = models.CharField(max_length=500, default='Any reason')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Evidence(models.Model):
    metric = models.ForeignKey(
        Metric,
        on_delete=models.CASCADE,
        related_name='evidences')
    slug = models.TextField(max_length=280)
    name = models.CharField(max_length=200, default='Evidence')
    is_valid = models.IntegerField(default=0)
    is_invalid = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
