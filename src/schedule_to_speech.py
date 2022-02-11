import datetime
import random

WEEKDAY_LIST = ["понедельник ", "вторник ", "среду ", "четверг ", "пятницу ", "субботу ", "воскресенье "]
TIPS_LIST = ["Чтобы выбрать другую группу, скажите \"Смена группы\" или \"Смена института\".",
             "Еще я могу рассказать расписание для выбранной даты.",
             "Я могу сохранить выбранную группу, вдруг пригодиться. Скажите \"Сохрани группу\"."]
MONTH_LIST = ["января ", "февраля ", "марта ", "апреля ", "мая ", "июня ", "июля ", "августа ", "сентября ", "октября ",
              "ноября ", "декабря "]


def transform_date(date):
    _, m, d = date.split("-")
    return f"{d} {MONTH_LIST[int(m) - 1]}"


def translate_day(day):
    text = ""
    text += "В"
    text += "o " if day['weekday'] == 2 else " "
    text += WEEKDAY_LIST[day['weekday'] - 1]
    text += transform_date(day['date'])
    tts = text
    count = len(day['lessons'])
    text += f"{count} "
    if count == 0:
        text += "пар. "
        tts += "нет пар. "
    elif count == 1:
        text += "пара. "
        tts += "одна пара. "
    elif count == 2:
        text += "пары. "
        tts += "две пары. "
    elif count < 5:
        text += "пары. "
        tts += f"{count} пары. "
    else:
        text += "пар. "
        tts += f"{count} пар. "

    for lesson in day['lessons']:
        time_start = lesson.get('time_start')
        if time_start is not None:
            text += f"С {time_start} "
            tts += f"С {time_start.split(':')[0]} "
        time_end = lesson.get('time_end')
        if time_end is not None:
            text += f"до {lesson['time_end']} {lesson['subject'].lower()}, {lesson['typeObj']['name'].lower()}. "
            tts += f"до {lesson['time_end']} {lesson['subject'].lower()}, {lesson['typeObj']['name'].lower()}. "
        teachers = lesson.get('teachers')
        if teachers is not None:
            text += f"Преподаватель - {lesson['teachers'][0]['full_name']}. "
            tts += f"Преподаватель - {lesson['teachers'][0]['full_name']}. "
        auditories = lesson.get('auditories')
        if auditories is not None:
            if auditories[0]['name'] == 'Дистанционно':
                text += "Занятие дистанционно."
                tts += "Занятие дистанционно."
            elif auditories[0]['name'] == 'Нет':
                text += "Аудитория не указана."
                tts += "Аудитория не указана."
            else:
                text += f"{auditories[0]['building']['name']}, аудитория {auditories[0]['name']}."
                tts += f"{auditories[0]['building']['name']}, аудитория {auditories[0]['name']}."
        text += "\n"
        tts += "\n"
    return text, tts


def translate(schedule, date=datetime.datetime.now().strftime("%Y-%m-%d")):
    text = ""
    tts = ""
    day = next((item for item in schedule if item["date"] == date), None)
    if day is None:
        if date == datetime.datetime.now().strftime("%Y-%m-%d"):
            text += "Сегодня нет пар.\n"
            tts += "Сегодня нет пар.\n"
        else:
            text += "В этот день нет пар.\n"
            tts += "В этот день нет пар.\n"
    else:
        (day_text, day_tts) = translate_day(day)
        text += day_text
        tts += day_tts
    random_tip = random.choice(TIPS_LIST)
    text += random_tip
    tts += random_tip
    return text, tts
