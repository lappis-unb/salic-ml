from django.core.management.base import BaseCommand
from analysis.preload_data import load_project_metrics


class Command(BaseCommand):
    help = 'Updates all saved projects finance metrics and indicator'

    def handle(self, *args, **kwargs):
        load_project_metrics()
        self.stdout.write("Finished updating projects metrics")
