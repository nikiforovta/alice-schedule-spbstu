WEEKDAY_ARRAY = ["понедельник ", "вторник ", "среду ", "четверг ", "пятницу ", "субботу ", "воскресенье "]


def transform_date(date):
    return "-".join(date.split("-")[::-1])


def translate_day(day):
    res = ""
    res += "В"
    res += "o " if day['weekday'] == 2 else " "
    res += WEEKDAY_ARRAY[day['weekday'] - 1]
    res += transform_date(day['date']) + " "
    count = len(day['lessons'])
    if count == 0:
        res += "нет пар. "
    elif count == 1:
        res += f"{count} пара. "
    elif count < 5:
        res += f"{count} пары. "
    else:
        res += f"{count} пар. "

    for lesson in day['lessons']:
        time_start = lesson.get('time_start')
        if time_start is not None:
            res += f"С {time_start} "
        time_end = lesson.get('time_end')
        if time_end is not None:
            res += f"до {lesson['time_end']} {lesson['subject'].lower()}, {lesson['typeObj']['name'].lower()}. "
        teachers = lesson.get('teachers')
        if teachers is not None:
            res += f"Преподаватель - {lesson['teachers'][0]['full_name']}. "
        auditories = lesson.get('auditories')
        if auditories is not None:
            if auditories[0]['name'] == 'Дистанционно':
                res += "Занятие дистанционно."
            elif auditories[0]['name'] == 'Нет':
                res += "Аудитория не указана. "
            else:
                res += f"{auditories[0]['building']['name']}, аудитория {auditories[0]['name']}. "
        res += "\n"
    return res


def translate(schedule, date=None):
    res = ""
    if date is not None:
        day = next((item for item in schedule if item["date"] == date), None)
        if day is None:
            res += "В этот день нет пар.\n"
        else:
            res += translate_day(day)
        res += "Чтобы выбрать другую группу, скажите \"Смена группы\" или \"Смена института\"."
    else:
        if len(schedule) > 0:
            day = schedule[0]
            res += translate_day(day)
        else:
            res += "На этой неделе нет пар.\n"
        res += "Еще я могу рассказать расписание для выбранной даты.\n"

    return res
