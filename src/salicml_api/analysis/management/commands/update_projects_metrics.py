from django.core.management.base import BaseCommand
from analysis.preload_data import load_project_metrics
from analysis.models import FinancialIndicator, AdmissibilityIndicator


class Command(BaseCommand):
    help = 'Updates all saved projects finance metrics and indicator'

    def handle(self, *args, **kwargs):
        load_project_metrics(FinancialIndicator)
        load_project_metrics(AdmissibilityIndicator)
        self.stdout.write("Finished updating projects metrics")
