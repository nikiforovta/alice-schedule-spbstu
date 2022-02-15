from ..datetime_operations import translate_datetime

relative_datetime_examples = [{
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 1
    },
    "value": {
        "day": -1,
        "day_is_relative": True
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 2
    },
    "value": {
        "day": -7,
        "day_is_relative": True
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 1
    },
    "value": {
        "day": 0,
        "day_is_relative": True
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 3
    },
    "value": {
        "year": -1,
        "year_is_relative": True
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 2
    },
    "value": {
        "month": 1,
        "month_is_relative": True
    }
}
]

absolute_datetime_examples = [{
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 2
    },
    "value": {
        "month": 5,
        "day": 20,
        "month_is_relative": False,
        "day_is_relative": False
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 3
    },
    "value": {
        "year": 2022,
        "month": 2,
        "day": 31,  # 31 февраля (?), необходима валидация даты, полученной в запросе
        "year_is_relative": False,
        "month_is_relative": False,
        "day_is_relative": False
    }
}, {
    "type": "YANDEX.DATETIME",
    "tokens": {
        "start": 0,
        "end": 3
    },
    "value": {
        "year": 2020,
        "month": 4,
        "day": 1,
        "year_is_relative": False,
        "month_is_relative": False,
        "day_is_relative": False
    }
}
]

mixed_datetime_examples = [
    {
        "type": "YANDEX.DATETIME",
        "tokens": {
            "start": 0,
            "end": 4
        },
        "value": {
            "year": -1,
            "month": 3,
            "day": 20,
            "year_is_relative": True,
            "month_is_relative": False,
            "day_is_relative": False
        }
    }
]


def test_translate_datetime():
    for d in relative_datetime_examples:
        print(translate_datetime(d))

    for d in absolute_datetime_examples:
        print(translate_datetime(d))

    for d in mixed_datetime_examples:
        print(translate_datetime(d))
