import datetime
from time import strptime

from datetime_operations import lessons_time

WEEKDAY_LIST = ["понедельник ", "вторник ", "среду ", "четверг ", "пятницу ", "субботу ", "воскресенье "]
MONTH_LIST = ["января ", "февраля ", "марта ", "апреля ", "мая ", "июня ", "июля ", "августа ", "сентября ", "октября ",
              "ноября ", "декабря "]


def transform_date(date):
    _, m, d = date.split("-")
    return f"{d} {MONTH_LIST[int(m) - 1]}"


def translate_day(day, current=True):
    if not current:
        text = "В"
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
    else:
        text = "Сегодняшние занятия."
        tts = text

    for lesson in day['lessons']:
        time_start = lesson.get('time_start')
        time_end = lesson.get('time_end')
        if time_end:
            if current and lessons_time(time_end) or not current:
                if time_start is not None:
                    text += f"С {time_start} "
                    tts += f"С {time_start.split(':')[0]} "
                if time_end is not None:
                    text += f"до {time_end} {lesson['subject']}"
                    tts += f"до {time_end} {lesson['subject'].lower()}"
                text += f", {lesson['typeObj']['name'].lower()}. "
                tts += f", {lesson['typeObj']['name'].lower()}. "
                teachers = lesson.get('teachers')
                if teachers is not None:
                    text += f"Преподаватель - {teachers[0]}. "
                    tts += f"Преподаватель - {teachers[0]}. "
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


def translate(schedule_day, date=datetime.datetime.now().strftime("%Y-%m-%d")):
    text = ""
    tts = ""
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if schedule_day is None:
        if date == today:
            text += "Сегодня нет пар.\n"
            tts += "Сегодня нет пар.\n"
        elif date < today:
            text += "В этот день не было пар.\n"
            tts += "В этот день не было пар.\n"
        else:
            text += "В этот день не будет пар.\n"
            tts += "В этот день не будет пар.\n"

    else:
        if strptime(schedule_day["date"], "%Y-%m-%d") == today:
            (day_text, day_tts) = translate_day(schedule_day)
        else:
            (day_text, day_tts) = translate_day(schedule_day, current=False)
        text += day_text
        tts += day_tts
    return text, tts
