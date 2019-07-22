PROJECT_DETAIL_URL = '/'

def test_project_detail(api_client):
    response = api_client.get(PROJECT_DETAIL_URL)
    assert(response.status_code == 200)
