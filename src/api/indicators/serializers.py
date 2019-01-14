from .models import Entity, Indicator, Metric, MetricFeedback, ProjectFeedback, User
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email')


class EntitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entity
        fields = ('pronac', 'name')


class IndicatorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Indicator
        fields = ('name', 'value', 'entity')


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ('value', 'name', 'reason', 'indicator')


class MetricFeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricFeedback
        fields = ('grade', 'reason', 'user', 'metric')


class ProjectFeedbackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProjectFeedback
        fields = ('grade', 'user', 'entity')


class TestSerializer(serializers.Serializer):
    test = serializers.CharField()
