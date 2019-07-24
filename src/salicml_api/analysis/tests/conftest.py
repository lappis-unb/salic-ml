import pytest
from django.test.client import Client
from rest_framework.test import APIClient
from django.db import connection
import os

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture(scope='session')
def django_db_modify_db_settings():
    os.environ['TEST_DB'] = "True"
    os.system("inv db-test")
    os.system("inv set-data")
    os.system("inv train-metrics")
    os.environ['TEST_DB'] = "False"