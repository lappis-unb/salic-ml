import logging

from boogie.rest import rest_api
from django.db import models
from sidekick import lazy
from salicml.data.db_operations import DATA_PATH
from salicml_api.analysis.situations import SITUATIONS
from django.contrib.contenttypes.models import ContentType

log = logging.getLogger("salic-ml.data")
LOG = log.info
MODEL_FILE = DATA_PATH / "scripts" / "models" / "general_project_data.sql"


class ProjectManager(models.Manager):
    def get_queryset(self):
        ordered = (
            super(ProjectManager, self)
            .get_queryset()
            .all()
            .order_by("-indicator__value")
        )
        return ordered


@rest_api(["pronac", "nome", "responsavel", "verified_funds",
           "raised_funds"], lookup_field="pronac")
class Project(models.Model):
    pronac = models.CharField(max_length=15, primary_key=True)
    nome = models.CharField(max_length=200)
    start_execution = models.DateTimeField(null=True)
    end_execution = models.DateTimeField(null=True)
    situation = models.CharField(choices=SITUATIONS, default="A01", max_length=200)
    description = models.CharField(max_length=200, null=True)
    responsavel = models.CharField(max_length=200, null=True)
    verified_funds = models.FloatField(null=True, blank=True, default=0.0)
    raised_funds = models.FloatField(null=True, blank=True, default=0.0)
    complexity = models.FloatField(null=True, blank=True, default=0.0)
    objects = ProjectManager()

    class Meta:
        app_label = "analysis"
        verbose_name_plural = "projetos"

    @lazy
    def complexidade(self):
        """
        Project complexity, same as FinancialIndicator value
        """
        return self.complexity

    def financial_indicator(self):
        """
        Project complexity, same as FinancialIndicator value
        """

        indicators = self.indicator_set.all()
        financial_indicator = None
        for indicator in indicators:
            if ContentType.objects.get(app_label='analysis', model='financialindicator').id == indicator.polymorphic_ctype_id:
                financial_indicator = indicator
                break
    
        return financial_indicator

    def __str__(self):
        return self.nome
