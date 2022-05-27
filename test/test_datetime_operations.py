import datetime

import pytest
from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from src.datetime_operations import translate_datetime


@pytest.mark.parametrize("relative_datetime, result",
                         [("вчера", (today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")),
                          ("неделю назад", (today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")),
                          ("сегодня", today().strftime("%Y-%m-%d")),
                          ("год назад", (today() - relativedelta(years=1)).strftime("%Y-%m-%d")),
                          ("через месяц", (today() + relativedelta(months=1)).strftime("%Y-%m-%d"))
                          ])
def test_translate_relative_datetime(relative_datetime, result):
    assert translate_date_marussia(relative_datetime) == result


@pytest.mark.parametrize("absolute_datetime, result",
                         [("20 мая", datetime.date(year=today().year, month=5, day=20).strftime("%Y-%m-%d")),
                          ("31 февраля 2022", None),
                          ("1 апреля 2020 года",
                           datetime.date(year=2020, month=4, day=1).strftime("%Y-%m-%d"))])
def test_translate_absolute_datetime(absolute_datetime, result):
    assert translate_date_marussia(absolute_datetime) == result


@pytest.mark.xfail(raises=AssertionError, reason="Эта библиотека так не умеет")
@pytest.mark.parametrize("mixed_datetime, result", [("20 марта прошлого года",
                                                     (datetime.date(year=today().year, month=3, day=20)
                                                      - relativedelta(years=1)).strftime("%Y-%m-%d"))])
def test_translate_mixed_datetime(mixed_datetime, result):
    assert translate_date_marussia(mixed_datetime) == result
