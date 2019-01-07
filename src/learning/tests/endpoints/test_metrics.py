import pytest

from salicml.api import main as salicml
from salicml.middleware.middleware import Middleware
from salicml.data_source.data_source_db import DataSourceMock

OK_CODE = 200
BAD_CODE = 400


def get_data_source():
    planilha_orcamentaria = [
        ["012345", 123, "2A"],
        ["012345", 124, "2A"],
        ["012345", 125, "2A"],
        ["012348", 126, "3A"],
        ["012348", 127, "3A"],
    ]
    data_source = DataSourceMock(planilha_orcamentaria=planilha_orcamentaria)

    set_planilha_aprovacao_comprovacao(data_source)
    return data_source


def set_planilha_aprovacao_comprovacao(data_source):
    NEEDED_COLUMNS = ["PRONAC", "Item", "vlAprovado", "vlComprovacao"]
    DATASET = [
        NEEDED_COLUMNS,
        ["123456", "Coca cola", 100, 149],
        ["123456", "Coca cola", 100, 150],
        ["123456", "Coca cola zero", 100, 151],
        ["123456", "Coca cola zero", 100, 152],
        ["123457", "Mouse", 100, 50],
        ["123458", "Teclado", 10, 3],
    ]
    data_source.set_planilha_aprovacao_comprovacao(DATASET)


@pytest.fixture
def client():
    app = salicml.app

    data_source = get_data_source()
    middleware = Middleware(data_source=data_source)
    middleware.load_all()

    app.middleware = middleware
    client = salicml.app.test_client()

    yield client  # TearDown code is below, SetUp code is above

    pass


def test_number_of_item_endpoint_keys(client):
    """"""
    pronac = "012345"
    endpoint = "metric/number_of_items/{}".format(pronac)
    response = client.get(endpoint)
    result = response.json

    assert response.status_code == OK_CODE

    expected_keys = [
        "is_outlier",
        "maximum_expected",
        "minimum_expected",
        "number_of_items",
    ]

    for key in expected_keys:
        assert key in result

    assert len(result) == len(expected_keys)


def test_number_of_items_endpoint_invalid_pronac(client):
    pronac = "123a45"
    endpoint = "metric/number_of_items/{}".format(pronac)
    response = client.get(endpoint)
    assert response.status_code == BAD_CODE


def test_verified_approved_endpoint_keys(client):
    """"""
    pronac = "123456"
    endpoint = "metric/verified_approved/{}".format(pronac)

    response = client.get(endpoint)
    result = response.json

    assert response.status_code == OK_CODE

    expected_keys = [
        "is_outlier",
        "maximum_expected",
        "minimum_expected",
        "number_of_outliers",
        "outlier_items",
    ]

    for key in expected_keys:
        assert key in result

    assert len(result) == len(expected_keys)


def test_verified_approved_endpoint_values(client):
    """"""
    pronac = "123456"
    endpoint = "metric/verified_approved/{}".format(pronac)

    response = client.get(endpoint)
    data = response.get_json()

    assert response.status_code == OK_CODE
    assert data["is_outlier"]
    assert data["maximum_expected"] == 0
    assert data["minimum_expected"] == 0
    assert data["number_of_outliers"] == 2
