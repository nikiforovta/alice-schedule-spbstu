import json

from src.main import handler

normal_dialog = [
    {
        "session": {
            "new": True
        },
        "request": {
            "original_utterance": ""
        },
        "state": {
            "application": {}
        },
        "version": "1.0"
    }
    ,
    {"session": {
        "new": False
    },
        "request": {
            "original_utterance": "икнт"
        },
        "state": {
            "application": {'faculty': None}
        },
        "version": "1.0"},
    {"session": {
        "new": False
    },
        "request": {
            "original_utterance": "3530203/10002"
        },
        "state": {
            "application": {'faculty': 'икнт'}
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
            "application": {
                'faculty': 'икнт',
                'group': '3530203/10002'}
        },
        "version": "1.0"}
]


def test_handler():
    for request in normal_dialog:
        print(json.loads(handler(request, None)))
    assert True
