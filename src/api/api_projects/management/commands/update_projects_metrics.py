from django.core.management.base import BaseCommand
from api_projects.preload_data import load_projects_metrics


class Command(BaseCommand):
    help = 'Updates all saved projects finance metrics and indicator'

    def handle(self, *args, **kwargs):
        load_projects_metrics()
        self.stdout.write("Finished updating projects metrics")
