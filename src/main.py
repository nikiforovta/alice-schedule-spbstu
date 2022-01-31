import json

from . import request_validation
from . import schedule_parser
from . import schedule_to_speech

sp = None


def handler(event, context):
    global sp
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
            group = event['state']['application'].get('group')
            if group:
                if rv.validate_date(answer):
                    response_json['response']['text'] = schedule_to_speech.translate(sp.get_schedule(answer), answer)
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
    return json.dumps(response_json)
