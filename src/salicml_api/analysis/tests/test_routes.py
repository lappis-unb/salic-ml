ROOT_URL = '/'
PROJECT_LIST_URL = '/v1/projects/'
PROJECT_DETAIL_URL = '/v1/projects/details'

def test_root_url(db, api_client):
    response = api_client.get(ROOT_URL)
    assert(response.status_code == 200)

def test_project_list_url(db, api_client):
    response = api_client.get(PROJECT_LIST_URL)
    print(response.content)
    assert(response.status_code == 201)

# def test_project_detail(api_client):
#     response = api_client.get(PROJECT_DETAIL_URL)
#     assert(response.status_code == 200)

# def test_project_detail_result(api_client):
#     response = api_client.get(PROJECT_DETAIL_URL)
#     print(response.content)
#     assert(response.status_code == 200)
