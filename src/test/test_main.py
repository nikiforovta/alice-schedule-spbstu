import json

from src import main

normal_dialog = [
    {
        "meta": {
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "account_linking": {},
                "payments": {},
                "screen": {}
            },
            "locale": "ru-RU",
            "timezone": "UTC"
        },
        "request": {
            "original_utterance": "сброс",
            "command": "",
            "nlu": {
                "entities": [],
                "tokens": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "session": {
            "message_id": 0,
            "new": True,
            "session_id": "ea6be08d-9794-4ae2-89e2-e94f6734cc65",
            "skill_id": "a8f78148-8184-4010-b508-ec70badddf82",
            "user_id": "94748746704CDF263F766BC5E1F0F9D68CD6DB739F2E7CCEF975EC7FCF2A9666",
            "user": {
                "user_id": "86507D953A1790E1F26F46ED4874098F7BC2658CFC9588F9CCC3E1DD9C061A95"
            },
            "application": {
                "application_id": "94748746704CDF263F766BC5E1F0F9D68CD6DB739F2E7CCEF975EC7FCF2A9666"
            }
        },
        "state": {
            "session": {},
            "user": {},
            "application": {}
        },
        "version": "1.0"
    },
    {
        "meta": {
            "locale": "ru-RU",
            "timezone": "UTC",
            "client_id": "ru.yandex.searchplugin/7.16 (none none; android 4.4.2)",
            "interfaces": {
                "screen": {},
                "payments": {},
                "account_linking": {}
            }
        },
        "session": {
            "message_id": 2,
            "session_id": "97aecec9-7ee8-4327-a47c-6905740e5e61",
            "skill_id": "b4650c20-82ab-45ad-bd26-d2aae92e40ea",
            "user": {
                "user_id": "9412254570D58A0F1F0CF25FEC75B20D09C3B0F3AA4DA94F49557F801C160685"
            },
            "application": {
                "application_id": "4FF410F6BC3708F9CD20BB8BBFAF817038ECF4206969F3FD11836D83F95BD6CE"
            },
            "new": False,
            "user_id": "4FF410F6BC3708F9CD20BB8BBFAF817038ECF4206969F3FD11836D83F95BD6CE"
        },
        "request": {
            "command": "икнт",
            "original_utterance": "3530901/80203",
            "nlu": {
                "tokens": [
                    "3530901",
                    "80203"
                ],
                "entities": [],
                "intents": {}
            },
            "markup": {
                "dangerous_context": False
            },
            "type": "SimpleUtterance"
        },
        "state": {
            "session": {},
            "user": {},
            "application": {"faculty": "икнт"}
        },
        "version": "1.0"
    },
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
                    "day": 2,
                    "day_is_relative": True
                }
            }]},
            "original_utterance": "2022-2-5"
        },
        "state": {
            "user": {},
            "application": {
                'faculty': 'икнт',
                'group': '3530901/80203'}
        },
        "version": "1.0"}
]


def test_handler():
    for request in normal_dialog:
        print(json.loads(main.handler(request, None)))
    assert True


group_examples = [
    ["3530901", "80203"], ["з", "3", "5", "3", "0", "9", "0", "1", "дробь", "8", "0", "2", "0", "3"],
    ["353", "0901", "слеш", "80203"], ["353", "09", "01", "8", "0", "2", "0", "3"], ['ooooo'], ['ooooooooooooo']
]


def test_group_recognition():
    for g in group_examples:
        print(main.group_recognition(g))
    assert True
