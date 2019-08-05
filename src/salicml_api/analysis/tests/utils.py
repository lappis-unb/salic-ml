import json

def load_json(response):
    return json.loads(response.content.decode('utf-8'))