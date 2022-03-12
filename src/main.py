import json
import random
import threading

import yaml

import group_operations
import schedule_parser
from data_gathering import gather_info


def generate_response(event):
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'end_session': False,
            'text': '',
            'tts': '',
            'buttons': [],
        },
        'user_state_update': {},
        'application_state': {}
    }


def greeting(teacher, faculty, group, possible_greetings):
    if teacher is not None:
        reply = random.choice(possible_greetings['OK']['TEACHER'])
        return f"{reply} {teacher}", f"{reply} {teacher}"
    if faculty is not None:
        if group is not None:
            reply = random.choice(possible_greetings['OK']['GROUP'])
            return f"{reply} {group} ({faculty}).\n", f"{reply} {' '.join(group)} ({' '.join(faculty)}). "
        else:
            reply = random.choice(possible_greetings['NO_GROUP'])
            return f"{reply} {faculty}).", f"{reply} {' '.join(faculty)}). "
    reply = random.choice(possible_greetings['NO_DATA'])
    return reply, reply


def handler(event, context, requests="requests.yaml", replies="replies.yaml"):
    teacher = event['state']['application'].get('teacher')
    faculty = event['state']['application'].get('faculty')
    group = event['state']['application'].get('group')
    sp = schedule_parser.ScheduleParser(teacher, faculty, group)
    background_sp = schedule_parser.ScheduleParser()
    response_json = generate_response(event)
    response_json['application_state']['group'] = group if group else None
    response_json['application_state']['faculty'] = faculty if faculty else None
    with open(requests, "r", encoding='utf8') as preq:
        with open(replies, "r", encoding='utf8') as prep:
            possible_requests = yaml.safe_load(preq)
            possible_replies = yaml.safe_load(prep)
        if event['session']['new']:
            (response_json['response']['text'], response_json['response']['tts']) = greeting(teacher, faculty, group,
                                                                                             possible_replies[
                                                                                                 "GREETING"])
            threading.Thread(target=group_operations.update_schedule, args=(event, background_sp))
        output_text, output_tts = gather_info(event, response_json, teacher, faculty, group, sp, possible_requests,
                                              possible_replies)
        response_json['response']['text'] += output_text
        response_json['response']['tts'] += output_tts
        return json.dumps(response_json)
