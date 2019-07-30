import pytest
from django.test.client import Client
from rest_framework.test import APIClient
import os
from django.core.management import call_command

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            call_command('create_models_from_sql', '--offline', 'True')
            os.system("inv set-data")
            call_command('update_projects_metrics')

