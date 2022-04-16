import json

from src import main


def test_handler():
    with open('request.json', 'rb') as request_examples:
        for request in json.load(request_examples):
            print(json.loads(main.handler(request, None)))
    assert True
