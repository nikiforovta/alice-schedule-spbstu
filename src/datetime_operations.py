import datetime
import time

from dateutil.relativedelta import relativedelta


def translate_date_marussia(day):
    nowadays = datetime.datetime.now()
    if day == 'вчера':
        return (datetime.datetime(nowadays.year, nowadays.month, nowadays.day) + relativedelta(days=-1)).strftime("%Y-%m-%d")
    elif day == 'сегодня':
        return nowadays.strftime("%Y-%m-%d")
    elif day == 'завтра':
        return (datetime.datetime(nowadays.year, nowadays.month, nowadays.day) + relativedelta(days=1)).strftime("%Y-%m-%d")
    else:
        return None


def translate_datetime(date):
    now = datetime.datetime.now()
    dy, dm, dd = 0, 0, 0
    year = date['value'].get('year')
    if year is not None:
        if date['value'].get('year_is_relative'):
            dy = year
            year = now.year
    else:
        year = now.year
    month = date['value'].get('month')
    if month is not None:
        if date['value'].get('month_is_relative'):
            dm = month
            month = now.month
    else:
        month = now.month
    day = date['value'].get('day')
    if day is not None:
        if date['value'].get('day_is_relative'):
            dd = day
            day = now.day
    else:
        day = now.day
    try:
        res = (datetime.datetime(year, month, day) + relativedelta(years=dy, months=dm, days=dd)).strftime("%Y-%m-%d")
        return res
    except ValueError:
        return None


def lessons_time(time_end):
    return time.strptime(time_end, "%H:%m") >= time.strptime(datetime.datetime.now().strftime("%H:%m"), "%H:%m")
