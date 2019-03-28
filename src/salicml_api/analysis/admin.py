from django.contrib import admin
from .models import Project, Metric, FinancialIndicator


admin.site.register(Project)
admin.site.register(FinancialIndicator)
admin.site.register(Metric)
