import logging

from boogie.rest import rest_api
from django.db import models
from salicml.data.db_operations import DATA_PATH
from salicml_api.analysis.situations import SITUATIONS

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


@rest_api(["pronac", "nome", "responsavel"], lookup_field="pronac")
class Project(models.Model):
    pronac = models.CharField(max_length=10, primary_key=True)
    nome = models.CharField(max_length=200)
    start_execution = models.CharField(null=True, max_length=200)
    end_execution = models.CharField(null=True, max_length=200)
    situation = models.CharField(choices=SITUATIONS, default="A01", max_length=200)
    description = models.CharField(max_length=200, null=True)
    responsavel = models.CharField(max_length=200, null=True)

    objects = ProjectManager()

    class Meta:
        app_label = "analysis"
        verbose_name_plural = "projetos"

    def __str__(self):
        return self.nome


"""
     1 - project.Project.objects.values_list('pk', 'indicator_set__metrics__name')
    
     2 - product(set(project.Project.objects.all().values_list('pk', flat=True)), set(['a', 'b']))
    
    set(project.Project.objects.values_list('pk', 'indicator_set__metrics__name')) 
    - 
    set(product(set(project.Project.objects.values_list('pk', flat=True)), set(['metric teste2', 'metric teste'])))
    
    #################
    
    projects_tp = project.Project.objects.values_list('pk', 'indicator_set__metrics__name')
    projects = [ p for p, _ in projects_tp]
    
    set(product(projects, ['metric teste2', 'metric teste']))
    - 
    set(projects_tp)
    
    def missing_metrics():
        existent_metrics = project.Project.objects.values_list('pk', 'indicator_set__metrics__name')
        all_projects = [ pk for pk, _ in existent_metrics]
        all_metrics = ['metric teste2', 'metric teste']
        
        return (
            set(product(all_projects, all_metrics)) - 
            set(existent_metrics)
        )
"""