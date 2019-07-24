import pytest
from django.test.client import Client
from rest_framework.test import APIClient
from django.db import connection
import os
from django.core.management import call_command

@pytest.fixture
def api_client():
    return APIClient()

#@pytest.fixture(scope='session')
#def django_db_modify_db_settings():
#    os.environ['TEST_DB'] = "True"
#    os.system("inv manager test") 
#    os.system("inv db-test")
#    os.system("inv set-data")
#    os.system("inv train-metrics")
#    os.environ['TEST_DB'] = "False"

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
        with django_db_blocker.unblock():
            call_command('loaddata', '/data/dump/dev_project.json')
            os.system("inv set-data")
            os.system("inv train_metrics")

