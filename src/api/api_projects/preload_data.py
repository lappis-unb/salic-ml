"""
Pre loads measurements from database saved projects
"""
from salicml.data.query import metrics as metrics_calc
from api_projects.models import Project


def load_metrics():
    #projects = Project.objects.all()
    #for project in projects:
    project = Project.objects.first()
    print(project.pronac)
    p_metrics = metrics_calc.get_project(project.pronac)
    print(p_metrics.finance.approved_funds)
