import json

import pytest

from main import group_recognition
from src import main


def test_handler():
    with open('request.json', 'rb') as request_examples:
        for request in json.load(request_examples):
            print(json.loads(main.handler(request, None, replies="../replies.yaml", requests="../requests.yaml")))
    assert True


@pytest.mark.parametrize("answer, possible_group", [(["3530901", "80203"], "3530901/80203"), (
        ["з", "3", "5", "3", "0", "9", "0", "1", "дробь", "8", "0", "2", "0", "3"], "з3530901/80203"),
                                                    (["353", "0901", "слеш", "80203"], "3530901/80203"),
                                                    (["353", "09", "01", "8", "0", "2", "0", "3"], "3530901/80203"),
                                                    (['ooooo'], None), (['ooooooooooooo'], "oooooooo/ooooo")])
def test_group_recognition(answer, possible_group):
    assert group_recognition(answer) == possible_group
