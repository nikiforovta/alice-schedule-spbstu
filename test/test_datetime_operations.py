import datetime

import pytest
from dateutil.relativedelta import relativedelta
from dateutil.utils import today

from src.datetime_operations import translate_datetime


@pytest.mark.parametrize("relative_datetime, result", [({"value": {"day": -1, "day_is_relative": True}},
                                                        (today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")),
                                                       ({"value": {"day": -7, "day_is_relative": True}},
                                                        (today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")),
                                                       ({"value": {"day": 0, "day_is_relative": True}},
                                                        today().strftime("%Y-%m-%d")),
                                                       ({"value": {"year": -1, "year_is_relative": True}},
                                                        (today() - relativedelta(years=1)).strftime("%Y-%m-%d")),
                                                       ({"value": {"month": 1, "month_is_relative": True}},
                                                        (today() + relativedelta(months=1)).strftime("%Y-%m-%d"))
                                                       ])
def test_translate_relative_datetime(relative_datetime, result):
    assert translate_datetime(relative_datetime) == result


@pytest.mark.parametrize("absolute_datetime, result",
                         [({"value": {"month": 5, "day": 20, "month_is_relative": False, "day_is_relative": False}},
                           datetime.date(year=today().year, month=5, day=20).strftime("%Y-%m-%d")),
                          ({"value": {"year": 2022, "month": 2, "day": 31,
                                      "year_is_relative": False,
                                      "month_is_relative": False,
                                      "day_is_relative": False}},
                           None),
                          ({"value": {"year": 2020, "month": 4, "day": 1,
                                      "year_is_relative": False,
                                      "month_is_relative": False, "day_is_relative": False}},
                           datetime.date(year=2020, month=4, day=1).strftime("%Y-%m-%d"))])
def test_translate_absolute_datetime(absolute_datetime, result):
    assert translate_datetime(absolute_datetime) == result


@pytest.mark.parametrize("mixed_datetime, result", [({"value": {"year": -1, "month": 3, "day": 20,
                                                                "year_is_relative": True,
                                                                "month_is_relative": False,
                                                                "day_is_relative": False}},
                                                     (datetime.date(year=today().year, month=3, day=20)
                                                      - relativedelta(years=1)).strftime("%Y-%m-%d"))])
def test_translate_mixed_datetime(mixed_datetime, result):
    assert translate_datetime(mixed_datetime) == result
