import json

ROOT_URL = '/'

def test_root_url(db, api_client):
    response = api_client.get(ROOT_URL)

    json_data = load_json(response)

    print(json_data)

    assert(response.status_code == 200)
