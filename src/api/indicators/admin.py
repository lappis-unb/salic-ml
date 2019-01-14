from django.contrib import admin

from .models import Indicator, Entity, Evidence, Metric, MetricFeedback, User, ProjectFeedback

admin.site.register(Indicator)
admin.site.register(Entity)
admin.site.register(Evidence)
admin.site.register(Metric)
admin.site.register(User)
admin.site.register(MetricFeedback)
admin.site.register(ProjectFeedback)
