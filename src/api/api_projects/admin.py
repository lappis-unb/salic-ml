from django.contrib import admin
from api_projects.models import Project, FinancialIndicator, Metric, Evidence


admin.site.register(Project)
admin.site.register(FinancialIndicator)
admin.site.register(Evidence)
admin.site.register(Metric)
