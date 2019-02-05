from django.db import models, transaction, IntegrityError
from boogie.rest import rest_api
import logging
import datetime
from polymorphic.models import PolymorphicModel
from polymorphic.managers import PolymorphicManager
from picklefield.fields import PickledObjectField
from salicml.data.db_connector import db_connector
from salicml.data.db_operations import DATA_PATH
from salicml.data.query import metrics as metrics_calc
from .situations import SITUATIONS

log = logging.getLogger("salic-ml.data")
LOG = log.info
MODEL_FILE = DATA_PATH / 'scripts' / 'models' / 'general_project_data.sql'


@rest_api(['pronac', 'name', 'start_execution'], lookup_field='pronac')
class Project(models.Model):
    pronac = models.IntegerField(default=0, unique=True)
    name = models.CharField(max_length=200)
    start_execution = models.CharField(null=True, max_length=200)
    end_execution = models.CharField(null=True, max_length=200)
    situation = models.CharField(
        choices=SITUATIONS,
        default="A01",
        max_length=200,
    )
    stage = models.CharField(max_length=200, null=True)
    analist = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


def execute_project_models_sql_scripts():
    """
        Used to get project information from MinC database
        and convert to this application Project models.
        Uses bulk_create if database is clean
    """
    # TODO: Remove except and use ignore_conflicts
    # on bulk_create when django 2.2. is released
    with open(MODEL_FILE, 'r') as file_content:
        query = file_content.read()
        db = db_connector()
        query_result = db.execute_pandas_sql_query(query)
        db.close()
        try:
            Project.objects.bulk_create(
                (Project(**vals) for vals in query_result.to_dict('records')),
                # ignore_conflicts=True available on django 2.2.
            )
        except IntegrityError:
            # happens when there are duplicated projects
            LOG('Projects bulk_create failed, creating one by one...')
            with transaction.atomic():
                for item in query_result.to_dict('records'):
                    Project.objects.get_or_create(**item)


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

    def fetch_weighted_complexity(self, recalculate_metrics=False):
        """
        Calculates indicator value according to metrics weights
        Uses metrics in database
        args:
            recalculate_metrics: If true metrics values are updated before
                                 using weights
        """
        # TODO: implment metrics recalculation
        max_total = sum([self.metrics_weights[metric_name] for metric_name in
                         self.metrics_weights])
        total = 0
        if recalculate_metrics:
            self.calculate_indicator_metrics()
        for metric in self.metrics:
            if metric.name in self.metrics_weights and metric.is_outlier:
                total += self.metrics_weights[metric.name]

        value = total/max_total
        value = 1 - value

        final_value = "{:.1f}".format(value * 10)

        if final_value[-1] == '0':
            final_value = "{:.0f}".format(value * 10)
            final_value = int(final_value)
        else:
            final_value = float(final_value)
        self.value = final_value
        self.updated_at = datetime.datetime.now()
        return final_value


class FinancialIndicatorManager(PolymorphicManager):
    def create_indicator(self, project):
        """
        Creates FinancialIndicator object for a project, calculating
        metrics and indicator value
        """
        # TODO:If update is True, update project metrics if already exists
        indicator = FinancialIndicator.objects.create(project=project)
        p_metrics = metrics_calc.get_project(project.pronac)
        print(p_metrics.finance.approved_funds)
        for metric_name in FinancialIndicator.METRICS_NAMES:
            x = getattr(p_metrics.finance, metric_name)
            Metric.create(metric_name, x, indicator)

        indicator.fetch_weighted_complexity()
        return indicator


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
    METRICS_NAMES = ['items', 'to_verify_funds', 'proponent_projects',
                     'new_providers', 'verified_approved', 'raised_funds',
                     'verified_funds', 'approved_funds', 'common_items_ratio',
                     'total_receipts', 'items_prices']

    objects = FinancialIndicatorManager()

    @property
    def metrics_weights(self):
        return {
            'items': 1,
            'to_verify_funds': 5,
            'proponent_projects': 2,
            'new_providers': 1,
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
    is_outlier = models.BooleanField(null=True)
    data = PickledObjectField(null=True)
    name = models.CharField(max_length=200, default='Metric')
    reason = models.CharField(max_length=500, default='Any reason')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, name, data, indicator):
        is_outlier = data['is_outlier']
        del data['is_outlier']
        metric = cls(name=name, is_outlier=is_outlier, indicator=indicator,
                     data=data)
        return metric

    def __str__(self):
        return self.name
