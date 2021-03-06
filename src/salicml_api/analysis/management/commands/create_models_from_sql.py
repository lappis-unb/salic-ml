from django.core.management.base import BaseCommand
from analysis.models import execute_project_models_sql_scripts


class Command(BaseCommand):
    help = "Loads projects models from" "data/scripts/models/general_project_data.sql"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force", dest="force", help="Force update if models already exists"
        )
        parser.add_argument(
            "--offline", dest="offline", help="Avoids online db query and uses offline csv instead"
        )

    def handle(self, *args, **options):
        execute_project_models_sql_scripts(options.get("force", False), options.get("offline", False))

        self.stdout.write("Finished populating models Project")
