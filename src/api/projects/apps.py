from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    name = 'projects'
    api = None

    def ready(self):
        from . import api

        self.api = api
