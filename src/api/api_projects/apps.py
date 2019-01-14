from django.apps import AppConfig


class ApiProjectsConfig(AppConfig):
    name = 'api_projects'
    api = None

    def ready(self):
        from . import api

        self.api = api
