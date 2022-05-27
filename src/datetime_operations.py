import datetime
import time

import dateparser


def translate_date_marussia(day):
    date = dateparser.parse(day)
    return date.strftime("%Y-%m-%d") if date else date


def lessons_time(time_end):
    return time.strptime(time_end, "%H:%m") >= time.strptime(datetime.datetime.now().strftime("%H:%m"), "%H:%m")
