import json

from src.main import handler, group_recognition

normal_dialog = [
    {
        "session": {
            "new": True
        },
        "request": {
            "original_utterance": ""
        },
        "state": {
            "user": {'faculty': 'икнт',
                'group': '3530203/10002'}
        },
        "version": "1.0"
    }
    ,
    {"session": {
        "new": False
    },
        "request": {
            "original_utterance": "институт компьютерных наук и технологий"
        },
        "state": {
            "user": {'faculty': 'икнт',
                'group': '3530203/10002'}
        },
        "version": "1.0"},
    {"session": {
        "new": False
    },
        "request": {
            "original_utterance": "3530203/10002",
            "nlu": {"tokens": "3530203/10002"}
        },
        "state": {
            "user": {'faculty': 'институт компьютерных наук и технологий'}
        },
        "version": "1.0"},
    {"session": {
        "new": False
    },
        "request": {
            "nlu": {"entities": [{
                "type": "YANDEX.DATETIME",
                "tokens": {
                    "start": 0,
                    "end": 1
                },
                "value": {
                    "day": -1,
                    "day_is_relative": True
                }
            }]},
            "original_utterance": "2022-2-5"
        },
        "state": {
            "user": {
                'faculty': 'икнт',
                'group': '3530203/10002'}
        },
        "version": "1.0"}
]


def test_handler():
    for request in normal_dialog:
        print(json.loads(handler(request, None)))
    assert True


group_examples = [
    ["3530901", "80203"], ["з", "3", "5", "3", "0", "9", "0", "1", "дробь", "8", "0", "2", "0", "3"],
    ["353", "0901", "слеш", "80203"], ["353", "09", "01", "8", "0", "2", "0", "3"], ['ooooo'], ['ooooooooooooo']
]


def test_group_recognition():
    for g in group_examples:
        print(group_recognition(g))
    assert True
