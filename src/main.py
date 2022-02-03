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
        'user_state_update': {}
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
            output_text, output_tts = schedule_to_speech.translate(sp.get_schedule(date), date)
        else:
            output_text = "Некорректная дата, попробуйте заново."
            output_tts = "Некорректная дата, попробуйте заново."
            response_json['response']['end_session'] = True
    else:
        output_text = "Некорректная дата, попробуйте еще раз."
        output_tts = "Некорректная дата, попробуйте еще раз."
    return output_text, output_tts


def gather_group(event, response_json, faculty, sp, rv):
    group = event['state']['user'].get('group')
    if group:
        if event['session']['new']:
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
        else:
            (output_text, output_tts) = gather_date(event, response_json, sp)
    else:
        possible_group = group_recognition(event['request']['nlu']['tokens'])
        group_search = rv.validate_group(faculty, possible_group)
        if group_search == "не знаю такой":
            output_text = f"Ой, я {group_search}, попробуйте еще раз."
            output_tts = f"Ой, я {group_search}, попробуйте еще раз."
        elif group_search == "группа найдена":
            sp.set_group(possible_group)
            response_json['user_state_update']['group'] = possible_group
            output_text = schedule_to_speech.translate(sp.get_schedule())
            output_tts = schedule_to_speech.translate(sp.get_schedule())
        else:
            output_text = "Пожалуйста, уточните номер группы."
            output_tts = "Пожалуйста, уточните номер группы."
    return output_text, output_tts


def gather_info(event, response_json):
    faculty = event['state']['user'].get('faculty')
    group = event['state']['user'].get('group')
    sp = schedule_parser.ScheduleParser(faculty, group)
    rv = request_validation.RequestValidator()
    answer = event['request']['original_utterance'].lower()
    if faculty:
        if answer == 'смена группы':
            sp.set_group(None)
            response_json['user_state_update']['group'] = None
            output_text = "Назовите номер группы."
            output_tts = "Назовите номер группы."
        elif answer == 'смена института':
            sp.set_faculty(None)
            sp.set_group(None)
            response_json['user_state_update']['faculty'] = None
            response_json['user_state_update']['group'] = None
            output_text = "Назовите институт."
            output_tts = "Назовите институт."
        else:
            (output_text, output_tts) = gather_group(event, response_json, faculty, sp, rv)
    elif rv.validate_faculty(answer):
        sp.set_faculty(answer)
        response_json['user_state_update']['faculty'] = answer
        output_text = "И номер группы."
        output_tts = "И номер группы."
    else:
        output_text = "Ой, я такой не знаю, попробуйте еще раз."
        output_tts = "Ой, я такой не знаю, попробуйте еще раз."
    return output_text, output_tts


def handler(event, context):
    faculty = event['state']['user'].get('faculty')
    group = event['state']['user'].get('group')
    response_json = generate_response(event)
    if event['session']['new']:
        (response_json['response']['text'], response_json['response']['tts']) = greeting(faculty, group)
    output_text, output_tts = gather_info(event, response_json)
    response_json['response']['text'] += output_text
    response_json['response']['tts'] += output_tts
    return json.dumps(response_json)
