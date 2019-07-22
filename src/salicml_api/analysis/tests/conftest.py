import pytest
from django.test.client import Client


@pytest.fixture
def api_client():
    return Client()

