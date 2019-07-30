import json
from .utils import load_json

ROOT_URL = '/'
PROJECT_LIST_URL = '/v1/projects/'

def test_root_url(db, api_client):
    response = api_client.get(ROOT_URL)

    json_data = load_json(response)

    print(json_data)

    assert(response.status_code == 200)

def test_project_list_url(db, api_client):
    response = api_client.get(PROJECT_LIST_URL)

    json_data = load_json(response)

    # assert(False)   
    assert(response.status_code == 200)
    assert(isinstance(json_data['data'], list))
    assert(len(json_data['data']) == 15)  

def test_project_list_object_type(db, api_client):
    response = api_client.get(PROJECT_LIST_URL)

    json_data = load_json(response)

    first_project = json_data['data'][0]

    pronac = first_project['pronac']
    details_url = 'v1/projects/{0}/details'.format(pronac)

    assert(isinstance(first_project['nome'], str))
    assert(isinstance(first_project['responsavel'], str))
    assert(isinstance(first_project['pronac'], str))
    assert(details_url in first_project['links']['details'])
    assert(first_project['complexidade'] == 3.2)

def sort_test(api_client, parameter, result, minus_result):
    response = api_client.get(PROJECT_LIST_URL + '?order_by=' + parameter)
    minus_response = api_client.get(PROJECT_LIST_URL + '?order_by=-' + parameter)
    
    json_data = load_json(response)
    json_data_minus = load_json(minus_response)
    
    first_project = json_data['data'][0]
    first_project_minus = json_data_minus['data'][0]

    assert(first_project[parameter] == result)
    assert(first_project_minus[parameter] == minus_result)

def test_project_list_sort_by_complexity(db, api_client):
    sort_test(api_client, 'complexidade', 0.0, 3.2)

def test_project_list_sort_by_nome(db, api_client):
    sort_test(api_client, 'nome', "\"1\"", 'Zuzu in Progress')

def test_project_list_sort_by_pronac(db, api_client):
    sort_test(api_client, 'pronac', '000044', '997603')

def test_project_list_sort_by_responsavel(db, api_client):
    sort_test(api_client, 'responsavel', ' ', 'xxxxxxxxxxx')
