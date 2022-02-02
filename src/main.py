import json

from . import request_validation, datetime_operations
from . import schedule_parser
from . import schedule_to_speech


def group_recognition(tokens):
    group = ""
    if len(tokens) == 2:
        return "/".join(tokens)
    for token in tokens:
        try:
            int(token)
            group += token
        except ValueError:
            if token in ['/', '\\', 'дробь', 'косая', 'делить', 'слэш', 'слеш']:
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
            'end_session': False
        },
        'application_state': {}
    }


def greeting():
    return "Привет! Назови свой институт."


def gather_date(event, response_json, group, sp):
    sp.set_group(group)
    response_json['application_state']['group'] = group
    date = next(
        (item for item in event['request']['nlu']['entities'] if item['type'] == "YANDEX.DATETIME"), None)
    if date is not None:
        date = datetime_operations.translate_datetime(date)
        if date is not None:
            response_json['response']['text'] = schedule_to_speech.translate(sp.get_schedule(date), date)
        else:
            response_json['response']['text'] = "Некорректная дата, попробуйте заново."
            response_json['response']['end_session'] = True
    else:
        response_json['response']['text'] = "Некорректная дата, попробуйте еще раз."


def gather_group(event, response_json, faculty, sp, rv):
    group = event['state']['application'].get('group')
    if group:
        gather_date(event, response_json, group, sp)
    else:
        possible_group = group_recognition(event['request']['nlu']['tokens'])
        group_search = rv.validate_group(faculty, possible_group)
        if group_search == "не знаю такой":
            response_json['response']['text'] = f"Ой, я {group_search}, попробуйте еще раз."
        elif group_search == "группа найдена":
            sp = schedule_parser.ScheduleParser(faculty, possible_group)
            response_json['response']['text'] = schedule_to_speech.translate(sp.get_schedule())
            response_json['application_state']['group'] = possible_group
        else:
            response_json['response']['text'] = "Пожалуйста, уточните номер группы."


def gather_info(event, response_json):
    sp = schedule_parser.ScheduleParser()
    rv = request_validation.RequestValidator()
    answer = event['request']['original_utterance'].lower()
    faculty = event['state']['application'].get('faculty')
    if faculty:
        if answer == 'смена группы':
            sp.set_faculty(faculty)
            response_json['application_state']['faculty'] = faculty
            response_json['response']['text'] = "Назовите номер группы."
        elif answer == 'смена института':
            sp.set_faculty(None)
            response_json['application_state']['faculty'] = ""
            response_json['response']['text'] = "Назовите институт."
        else:
            sp.set_faculty(faculty)
            response_json['application_state']['faculty'] = faculty
            gather_group(event, response_json, faculty, sp, rv)
    elif rv.validate_faculty(answer):
        response_json['response']['text'] = "И номер группы."
        response_json['application_state']['faculty'] = answer
    else:
        response_json['response']['text'] = "Ой, я такой не знаю, попробуйте еще раз."


def handler(event, context):
    response_json = generate_response(event)
    if event['session']['new']:
        response_json['response']['text'] = greeting()
    else:
        gather_info(event, response_json)
    response_json['response']['tts'] = response_json['response']['text']
    return json.dumps(response_json)
