def date_transform(old_date):
    y, m, d = old_date.split('-')
    m = f'0{m}' if len(m) == 1 else m
    d = f'0{d}' if len(d) == 1 else d
    return '-'.join((y, m, d))


WEEKDAY_ARRAY = ["понедельник ", "вторник ", "среду ", "четверг ", "пятницу ", "субботу ", "воскресенье "]


def translate_day(day):
    res = ""
    res += "В"
    res += "o " if day['weekday'] == 2 else " "
    res += WEEKDAY_ARRAY[day['weekday'] - 1]
    res += day['date'] + " "
    count = len(day['lessons'])
    if count == 0:
        res += "нет пар. "
    elif count == 1:
        res += "1 пара. "
    elif count < 5:
        res += f"{count} пары. "
    else:
        res += f"{count} пар. "

    for lesson in day['lessons']:
        res += f"C {lesson['time_start']} до {lesson['time_end']} {lesson['subject'].lower()}, " \
               f"{lesson['typeObj']['name'].lower()}. Преподаватель - {lesson['teachers'][0]['full_name']}. " \
               f"{lesson['auditories'][0]['building']['name']}, аудитория {lesson['auditories'][0]['name']}. "
        res += "\n"
    return res


def translate(schedule, date=None):
    res = ""
    if date is not None:
        date = date_transform(date)
        day = next((item for item in schedule if item["date"] == date), None)
        if day is None:
            res += "В этот день нет пар."
        else:
            res += translate_day(day)
    else:
        for day in schedule:
            res += translate_day(day)
            res += "Еще я могу рассказать расписание для выбранной даты.\n"

    return res
