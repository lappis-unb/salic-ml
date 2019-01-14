from django.db import models
from boogie.rest import rest_api


@rest_api(['pronac', 'name', 'created_at'], lookup_field='pronac')
class Project(models.Model):
    pronac = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name


@rest_api(['name', 'value'], inline=True)
class Indicator(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='indicator_set')
    name = models.CharField(max_length=200)
    value = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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
