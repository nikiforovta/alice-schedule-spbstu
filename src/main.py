import json

from . import request_validation, datetime_operations
from . import schedule_parser
from . import schedule_to_speech


def handler(event, context):
    sp = schedule_parser.ScheduleParser()
    response_json = {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'end_session': False
        },
        'application_state': {}
    }
    if event['session']['new']:
        response_json['response']['text'] = "Привет! Назови свой институт."
    else:
        answer = event['request']['original_utterance'].lower()
        rv = request_validation.RequestValidator()
        faculty = event['state']['application'].get('faculty')
        if faculty:
            response_json['application_state']['faculty'] = faculty
            sp.set_faculty(faculty)
            group = event['state']['application'].get('group')
            if group:
                sp.set_group(group)
                response_json['application_state']['group'] = group
                date = next(
                    item for item in event['request']['nlu']['entities'] if item['type'] == "YANDEX.DATETIME")
                if date is not None:
                    date = datetime_operations.translate_datetime(date)
                    if date is not None:
                        response_json['response']['text'] = schedule_to_speech.translate(sp.get_schedule(date), date)
                    else:
                        response_json['response']['text'] = "Некорректная дата, попробуйте еще раз."
                else:
                    response_json['response']['text'] = "Некорректная дата, попробуйте еще раз."
            else:
                group_search = rv.validate_group(faculty, answer)
                if group_search == "не знаю такой":
                    response_json['response']['text'] = f"Ой, я {group_search}."
                    response_json['end_session'] = True
                elif group_search == "группа найдена":
                    sp = schedule_parser.ScheduleParser(faculty, answer)
                    response_json['response']['text'] = schedule_to_speech.translate(sp.get_schedule())
                    response_json['application_state']['group'] = answer
                else:
                    response_json['response']['text'] = "Пожалуйста, уточните номер группы."
        elif rv.validate_faculty(answer):
            response_json['response']['text'] = "И номер группы."
            response_json['application_state']['faculty'] = answer
        else:
            response_json['response']['text'] = "Ой, я такой не знаю."
            response_json['end_session'] = True
    response_json['response']['tts'] = response_json['response']['text']
    return json.dumps(response_json)
