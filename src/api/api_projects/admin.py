from django.contrib import admin
from .models import Project, Indicator, Metric, Evidence


admin.site.register(Project)
admin.site.register(Indicator)
admin.site.register(Metric)
admin.site.register(Evidence)
