import json
import os.path

import main


def test_handler(repo_root):
    with open(os.path.join(repo_root, 'test/request.json'), 'rb') as request_examples:
        for request in json.load(request_examples):
            main.handler(request, None)
    assert True
