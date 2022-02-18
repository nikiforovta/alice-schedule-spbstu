import json
import random

import datetime_operations
import request_validation
import schedule_parser
import schedule_to_speech


def group_recognition(tokens):
    group = ""
    if len(tokens) == 2:
        return "/".join(tokens)
    for token in tokens:
        try:
            int(token)
            group += token
        except ValueError:
            if token in ['/', '\\', 'дробь', 'косая', 'деление', 'слэш', 'слеш']:
                group += '/'
            elif token in [',', 'черта']:
                continue
            else:
                group += token
    try:
        if group[-6] != '/':
            group = '/'.join([group[:-5], group[-5:]])
    except IndexError:
        return None
    return group


def generate_response(event):
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'end_session': False,
            'text': '',
            'tts': ''
        },
        'user_state_update': {},
        'application_state': {}
    }


def greeting(faculty, group):
    if faculty is None:
        return "Привет! Назови свой институт.", "Привет! Назови свой институт."
    elif group is None:
        return f"Привет! Назови номер своей группы (институт {faculty}).", f"Привет! Назови номер своей группы (" \
                                                                           f"институт {' '.join(faculty)}). "
    else:
        return f"Привет! Вот расписание для группы {group} (институт {faculty}).\n", f"Привет! Вот расписание для " \
                                                                                     f"группы {' '.join(group)} (" \
                                                                                     f"институт " \
                                                                                     f"{' '.join(faculty)}).\n "


def gather_date(event, response_json, sp):
    date = next(
        (item for item in event['request']['nlu']['entities'] if item['type'] == "YANDEX.DATETIME"), None)
    if date is not None:
        date = datetime_operations.translate_datetime(date)
        if date is not None:
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule(date), date)
        else:
            output_text = "Некорректная дата, попробуйте заново."
            output_tts = "Некорректная дата, попробуйте заново."
            response_json['response']['end_session'] = True
    else:
        output_text = "Некорректная дата, попробуйте еще раз."
        output_tts = "Некорректная дата, попробуйте еще раз."
    return output_text, output_tts


def save_group(event, response_json):
    saved_groups = event['state']['user'].get('saved_groups')
    if saved_groups:
        for saved_group in saved_groups:
            if saved_group['faculty'] == response_json['state']['application']['faculty'] and saved_group['group'] == \
                    response_json['state']['application']['group']:
                output_text = f"Группа {saved_group['group']} уже сохранена"
                output_tts = f"Группа {' '.join(saved_group['group'])} уже сохранена"
                return output_text, output_tts
        response_json['user_state_update']['saved_groups'].append(
            {"faculty": event['state']['application']['faculty'], "group": event['state']['application']['group']})
    else:
        response_json['user_state_update']['saved_groups'] = [
            {'faculty': event['state']['application']['faculty'], 'group': event['state']['application']['group']}]
    output_text = f"Группа {event['state']['application']['group']} сохранена"
    output_tts = f"Группа {' '.join(event['state']['application']['group'])} сохранена"
    return output_text, output_tts


def list_groups(event, tip=None):
    saved_groups = event['state']['user'].get('saved_groups')
    output_text = 'Пока вы не сохранили ни одну группу. Чтобы сохранить группу, выберите её и скажите "Сохрани группу"'
    output_tts = output_text
    if saved_groups:
        if len(saved_groups) > 0:
            output_text = "На данный момент сохранены следующие группы:\n"
            output_tts = output_text
            for i, saved_group in enumerate(event['state']['user']['saved_groups']):
                output_text += f"Номер {i + 1}: {saved_group['group']} (институт {saved_group['faculty']})\n"
                output_tts += f"Номер {i + 1}: {' '.join(saved_group['group'])} " \
                              f"(институт {' '.join(saved_group['faculty'])})\n "
            if tip:
                random_tip = random.choice(schedule_to_speech.TIPS_LIST)
                output_text += random_tip
                output_tts += random_tip
    return output_text, output_tts


def remove_group(event, response_json, index: int):
    _, g = event['state']['user']['saved_groups'][index - 1].values()
    output_text = f"Группа {g} удалена"
    output_tts = f"Группа {' '.join(g)} удалена"
    del event['state']['user']['saved_groups'][index - 1]
    response_json['user_state_update']['saved_groups'] = event['state']['user']['saved_groups']
    return output_text, output_tts


def remove_group_options(event, response_json):
    (output_text, output_tts) = list_groups(event)
    if len(event['state']['user']['saved_groups']) > 0:
        response_json['user_state_update']['intent_remove'] = True
        output_text += "\nВыберите номер группы для удаления."
        output_tts += "\nВыберите номер группы для удаления."
    return output_text, output_tts


def reset_settings(event, response_json, sp):
    response_json['session_state'] = None
    user_settings = event['state'].get('user')
    if user_settings:
        for k in user_settings.keys():
            response_json['user_state_update'][k] = None
    response_json['application_state'] = {}
    sp.set_faculty(None)
    sp.set_group(None)
    output_text = "Все настройки сброшены. Назовите институт"
    output_tts = "Все настройки сброшены. Назовите институт"
    return output_text, output_tts


def gather_group(event, response_json, faculty, sp, rv):
    group = event['state']['application'].get('group')
    answer = event['request']['original_utterance'].lower()
    if group:
        response_json['application_state']['group'] = group
        sp.set_group(group)
        if event['session']['new']:
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
        else:
            if "какие группы сохранены" in answer:
                (output_text, output_tts) = list_groups(event, tip=True)
            elif "сохрани группу" in answer:
                (output_text, output_tts) = save_group(event, response_json)
            elif "удали группу" in answer:
                (output_text, output_tts) = remove_group_options(event, response_json)
            else:
                (output_text, output_tts) = gather_date(event, response_json, sp)
    else:
        possible_group = group_recognition(event['request']['nlu']['tokens'])
        group_search = rv.validate_group(faculty, possible_group)
        if group_search == 0:
            output_text = "Ой, я не знаю такой группы, попробуйте еще раз."
            output_tts = "Ой, я не знаю такой группы, попробуйте еще раз."
        elif group_search == 1:
            sp.set_group(possible_group)
            response_json['application_state']['group'] = possible_group
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
        else:
            output_text = "Пожалуйста, уточните номер группы."
            output_tts = "Пожалуйста, уточните номер группы."
    return output_text, output_tts


STOP_WORDS_LIST = ["хватит", "стоп", "прекрати", "остановись"]
HELP_WORDS_LIST = ["помощь", "что ты умеешь", "как пользоваться"]
RESET_WORDS_LIST = ['сброс', 'сбрось']


def gather_info(event, response_json, faculty, group):
    sp = schedule_parser.ScheduleParser(faculty, group)
    rv = request_validation.RequestValidator()
    answer = event['request']['original_utterance'].lower()
    if any([stop_word in answer for stop_word in STOP_WORDS_LIST]):
        response_json['response']['end_session'] = True
        output_text, output_tts = "Выключаюсь", "Выключаюсь"
    elif any([help_word in answer for help_word in HELP_WORDS_LIST]):
        output_text, output_tts = "Навык позволяет узнать расписание выбранной группы в Санкт-Петербургском " \
                                  "Политехническом университете Петра Великого", "Навык позволяет узнать расписание " \
                                                                                 "выбранной группы в " \
                                                                                 "Санкт-Петербургском " \
                                                                                 "Политехническом университете Петра " \
                                                                                 "Великого"
    elif event['state']['user'].get('intent_remove'):
        possible_index = event['request']['nlu']['entities']
        index = -1
        for pi in possible_index:
            if pi['type'] == "YANDEX.NUMBER":
                index = int(pi['value'])
                break
        if index != -1:
            (output_text, output_tts) = remove_group(event, response_json, index)
        response_json['user_state_update']['intent_remove'] = False
    elif "сброс" in answer:
        (output_text, output_tts) = reset_settings(event, response_json, sp)
    elif faculty:
        response_json['application_state']['faculty'] = faculty
        sp.set_faculty(faculty)
        if answer == 'смена группы':
            sp.set_group(None)
            response_json['application_state']['group'] = None
            output_text = "Назовите номер группы."
            output_tts = "Назовите номер группы."
        elif answer == 'смена института':
            sp.set_faculty(None)
            sp.set_group(None)
            response_json['application_state']['faculty'] = None
            response_json['application_state']['group'] = None
            output_text = "Назовите институт."
            output_tts = "Назовите институт."
        else:
            (output_text, output_tts) = gather_group(event, response_json, faculty, sp, rv)
    elif rv.validate_faculty(answer):
        sp.set_faculty(answer)
        response_json['application_state']['faculty'] = answer if sp.set_faculty(answer) else sp.NAME_ABBR[
            answer.lower()]
        output_text = "И номер группы."
        output_tts = "И номер группы."
    elif answer == "":
        output_text = ""
        output_tts = ""
    else:
        output_text = "Ой, я такой институт не знаю, попробуйте еще раз."
        output_tts = "Ой, я такой институт не знаю, попробуйте еще раз."
    return output_text, output_tts


def handler(event, context):
    faculty = event['state']['application'].get('faculty')
    group = event['state']['application'].get('group')
    response_json = generate_response(event)
    if event['session']['new']:
        (response_json['response']['text'], response_json['response']['tts']) = greeting(faculty, group)
    output_text, output_tts = gather_info(event, response_json, faculty, group)
    response_json['response']['text'] += output_text
    response_json['response']['tts'] += output_tts
    return json.dumps(response_json)
