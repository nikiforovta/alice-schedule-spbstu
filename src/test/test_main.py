import json
import os.path

from src.main import handler


def test_handler(repo_root):
    with open(os.path.join(repo_root, 'request.json'), 'rb') as request_examples:
        for request in json.load(request_examples):
            print(json.loads(handler(request, None)))
    assert True
