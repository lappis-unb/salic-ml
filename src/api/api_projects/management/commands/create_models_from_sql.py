from django.core.management.base import BaseCommand
from api_projects.models import execute_project_models_sql_scripts


class Command(BaseCommand):
    help = ('Loads projects models from'
            'data/scripts/models/general_project_data.sql')

    def handle(self, *args, **kwargs):
        execute_project_models_sql_scripts()
        self.stdout.write("Finished populating models Project")
