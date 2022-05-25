import json
import os.path
import random

import yaml

from ..src import schedule_parser
from ..src.data_gathering import gather_info


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
        'session_state': event['state']['session']
    }


def greeting(faculty, group, possible_greetings):
    if faculty is not None:
        if group is not None:
            reply = random.choice(possible_greetings['OK']['GROUP'])
            return f"{reply} {group} ({faculty}).\n", f"{reply} {' '.join(group)} ({' '.join(faculty)}). "
        else:
            reply = random.choice(possible_greetings['NO_GROUP'])
            return f"{reply} {faculty}).", f"{reply} {' '.join(faculty)}). "
    reply = random.choice(possible_greetings['NO_DATA'])
    return reply, reply


def handler(event, context,
            requests=os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), "requests.yaml"),
            replies=os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), "replies.yaml")):
    response_json = generate_response(event)
    with open(requests, "r", encoding='utf8') as preq:
        possible_requests = yaml.safe_load(preq)
    with open(replies, "r", encoding='utf8') as prep:
        possible_replies = yaml.safe_load(prep)
    if event['session']['new']:
        saved = event['state']['user'].get('saved_groups')
        if saved and len(saved) > 0:
            faculty = saved[0]['faculty']
            group = saved[0]['group']
        else:
            faculty = None
            group = None
        (response_json['response']['text'], response_json['response']['tts']) = greeting(faculty, group,
                                                                                         possible_replies["GREETING"])
    else:
        faculty = event['state']['session'].get('faculty')
        group = event['state']['session'].get('group')
    response_json['session_state']['group'] = group
    response_json['session_state']['faculty'] = faculty
    sp = schedule_parser.ScheduleParser(faculty, group)
    output_text, output_tts = gather_info(event, response_json, faculty, group, sp, possible_requests, possible_replies)
    response_json['response']['text'] += output_text
    response_json['response']['tts'] += output_tts
    return json.dumps(response_json)
