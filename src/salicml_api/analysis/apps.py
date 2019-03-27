from django.apps import AppConfig


class AnalysisConfig(AppConfig):
    name = 'analysis'
    api = None

    def ready(self):
        from . import api

        self.api = api
