import json
import os.path
import random

import yaml

import schedule_parser
from buttons import group_buttons, additional_buttons
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
        'session_state': event['state']['session']
    }


def greeting(faculty, group, possible_greetings, sp, response_json):
    if faculty is not None:
        if group is not None:
            reply = random.choice(possible_greetings['OK']['GROUP'])
            return f"{reply} {group} ({faculty}).\n", f"{reply} {' '.join(group)} ({' '.join(faculty)}). "
        else:
            reply = random.choice(possible_greetings['NO_GROUP'])
            group_buttons(sp, response_json)
            return f"{reply}{faculty}). ", f"{reply}{' '.join(faculty)}). "
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
        user_data = event['state'].get('user')
        if user_data:
            saved = user_data.get('saved_groups')
            if saved and len(saved) > 0:
                faculty = saved[0]['faculty']
                group = saved[0]['group']
            else:
                faculty = None
                group = None
        else:
            faculty = None
            group = None
        response_json['session_state']['group'] = group
        response_json['session_state']['faculty'] = faculty
        sp = schedule_parser.ScheduleParser(faculty, group)
        (response_json['response']['text'], response_json['response']['tts']) = greeting(faculty, group,
                                                                                         possible_replies["GREETING"],
                                                                                         sp, response_json)
    else:
        session_data = event['state'].get('session')
        if session_data:
            faculty = session_data.get('faculty')
            group = session_data.get('group')
        else:
            faculty = None
            group = None
        response_json['session_state']['group'] = group
        response_json['session_state']['faculty'] = faculty
        sp = schedule_parser.ScheduleParser(faculty, group)
    output_text, output_tts = gather_info(event, response_json, faculty, group, sp, possible_requests, possible_replies)
    response_json['response']['text'] += output_text
    response_json['response']['tts'] += output_tts
    additional_buttons(response_json, possible_requests)
    return json.dumps(response_json)
