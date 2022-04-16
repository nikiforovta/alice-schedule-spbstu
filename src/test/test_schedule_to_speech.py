import json

import pytest

import schedule_to_speech


def test_translate():
    with open("schedule.json", "rb") as schedule:
        for day in json.load(schedule):
            assert schedule_to_speech.translate_day(day, current=False)[0] == day['result']


@pytest.mark.parametrize("date, result",
                         [("2022-02-24", "24 февраля "),
                          ("1939-09-01", "01 сентября "),
                          ("2035-02-29", "29 февраля "),
                          ("2018-12-31", "31 декабря ")])
def test_date_transform(date, result):
    assert result == schedule_to_speech.transform_date(date)
