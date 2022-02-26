import json

import pytest

from main import group_recognition
from src import main

normal_dialog = [
    {
        "request": {
            "original_utterance": "сброс",
            "command": "",
            "nlu": {
                "entities": [],
                "tokens": [],
                "intents": {}
            },
        },
        "session": {
            "new": True,
        },
        "state": {
            "session": {},
            "user": {},
            "application": {}
        },
        "version": "1.0"
    },
    {
        "session": {
            "new": False,
        },
        "request": {
            "command": "ИКНТ",
            "original_utterance": "3530901/80203",
            "nlu": {
                "tokens": [
                    "3530901",
                    "80203"
                ],
                "entities": [],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {},
            "application": {"faculty": "ИКНТ"}
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
                'faculty': 'ИКНТ',
                'group': '3530901/80203'}
        },
        "version": "1.0"},
    {

        "session": {
            "new": False,
        },
        "request": {
            "command": "1",
            "original_utterance": "первая",
            "nlu": {
                "tokens": [
                    "1"
                ],
                "entities": [
                    {
                        "type": "YANDEX.NUMBER",
                        "tokens": {
                            "start": 0,
                            "end": 1
                        },
                        "value": 1
                    }
                ],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ],
                "intent_remove": True
            },
            "application": {
                "faculty": "ИКНТ",
                "group": "3530901/80203"
            }
        },
        "version": "1.0"
    },
    {
        "session": {
            "new": False,
        },
        "request": {
            "command": "сохрани группу",
            "original_utterance": "сохрани группу",
            "nlu": {
                "tokens": [
                    "сохрани",
                    "группу"
                ],
                "entities": [],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ],
                "intent_remove": False
            },
            "application": {
                "faculty": "ИКНТ",
                "group": "3530203/10002"
            }
        },
        "version": "1.0"
    },
    {

        "session": {
            "new": True,

        },
        "request": {
            "command": "",
            "original_utterance": "",
            "nlu": {
                "tokens": [],
                "entities": [],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ],
                "intent_remove": False
            },
            "application": {
                "group": None,
                "faculty": None
            }
        },
        "version": "1.0"
    },
    {
        "session": {
            "new": False
        },
        "request": {
            "command": "353020310002",
            "original_utterance": "353020310002",
            "nlu": {
                "tokens": [
                    "353020310002"
                ],
                "entities": [
                    {
                        "type": "YANDEX.NUMBER",
                        "tokens": {
                            "start": 0,
                            "end": 1
                        },
                        "value": 353020310000
                    }
                ],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ],
                "intent_remove": False
            },
            "application": {
                "group": None,
                "faculty": "ИКНТ"
            }
        },
        "version": "1.0"
    },

    {
        "session": {
            "new": True
        },
        "request": {
            "command": "",
            "original_utterance": "",
            "nlu": {
                "tokens": [],
                "entities": [],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ],
                "intent_remove": False
            },
            "application": {
                "group": None,
                "faculty": "ИКНТ"
            }
        },
        "version": "1.0"
    },
    {
        "session": {
            "new": True
        },
        "request": {
            "command": "сброс",
            "original_utterance": "сброс",
            "nlu": {
                "tokens": [
                    "сброс"
                ],
                "entities": [],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {},
            "application": {
                "group": None,
                "faculty": "ИКНТ"
            }
        },
        "version": "1.0"
    },
    {
        "session": {
            "new": False
        },
        "request": {
            "command": "новопашенный андрей гелиевич",
            "original_utterance": "новопашенный андрей гелиевич",
            "nlu": {
                "tokens": [
                    "новопашенный",
                    "андрей",
                    "гелиевич"
                ],
                "entities": [
                    {
                        "type": "YANDEX.FIO",
                        "tokens": {
                            "start": 0,
                            "end": 3
                        },
                        "value": {
                            "first_name": "андрей",
                            "patronymic_name": "гелиевич",
                            "last_name": "новопашенный"
                        }
                    }
                ],
                "intents": {}
            },
        },
        "state": {
            "session": {},
            "user": {
                "saved_groups": [
                    {
                        "faculty": "ИКНТ",
                        "group": "3530901/80203"
                    }
                ]
            },
            "application": {
                "group": "3530901/80203",
                "faculty": "ИКНТ"
            }
        },
        "version": "1.0"
    }
]


def test_handler():
    for request in normal_dialog:
        print(json.loads(main.handler(request, None)))
    assert True


@pytest.mark.parametrize("answer, possible_group", [(["3530901", "80203"], "3530901/80203"), (
        ["з", "3", "5", "3", "0", "9", "0", "1", "дробь", "8", "0", "2", "0", "3"], "з3530901/80203"),
                                                    (["353", "0901", "слеш", "80203"], "3530901/80203"),
                                                    (["353", "09", "01", "8", "0", "2", "0", "3"], "3530901/80203"),
                                                    (['ooooo'], None), (['ooooooooooooo'], "oooooooo/ooooo")])
def test_group_recognition(answer, possible_group):
    assert group_recognition(answer) == possible_group
