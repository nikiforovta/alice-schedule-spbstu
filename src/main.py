import json
import random

import yaml

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


def teacher_recognition(value):
    return f'{value.get("last_name", "")} {value.get("first_name", "")} {value.get("patronymic_name", "")}'


def date_buttons(response_json):
    response_json['response']['buttons'].append({"title": "Вчера", "hide": True})
    response_json['response']['buttons'].append({"title": "Сегодня", "hide": True})
    response_json['response']['buttons'].append({"title": "Завтра", "hide": True})


def faculty_buttons(sp, response_json):
    for faculty in sp.FACULTY_LIST:
        response_json['response']['buttons'].append({"title": faculty["abbr"], "hide": True})


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


def gather_date(event, response_json, sp, possible_replies):
    date = next((item for item in event['request']['nlu']['entities'] if item['type'] == "YANDEX.DATETIME"), None)
    if date is not None:
        date = datetime_operations.translate_datetime(date)
        if date is not None:
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule(date), date)
            tip = random.choice(possible_replies['TIP'])
            output_text += tip
            output_tts += tip
        else:
            reply = random.choice(possible_replies["DATE"]["INCORRECT"])
            output_text = reply
            output_tts = reply
            response_json['response']['end_session'] = True
    else:
        reply = random.choice(possible_replies["DATE"]["INCORRECT"])
        output_text = reply
        output_tts = reply
    date_buttons(response_json)
    return output_text, output_tts


def save_group(event, response_json):
    saved_groups = event['state']['user'].get('saved_groups')
    if saved_groups:
        for saved_group in saved_groups:
            if saved_group['faculty'] == event['state']['application']['faculty'] and saved_group['group'] == \
                    event['state']['application']['group']:
                output_text = f"Группа {saved_group['group']} уже сохранена"
                output_tts = f"Группа {' '.join(saved_group['group'])} уже сохранена"
                return output_text, output_tts
        saved_groups.append(
            {"faculty": event['state']['application']['faculty'], "group": event['state']['application']['group']})
        response_json['user_state_update']['saved_groups'] = saved_groups
    else:
        response_json['user_state_update']['saved_groups'] = [
            {'faculty': event['state']['application']['faculty'], 'group': event['state']['application']['group']}]
    output_text = f"Группа {event['state']['application']['group']} сохранена."
    output_tts = f"Группа {' '.join(event['state']['application']['group'])} сохранена."
    return output_text, output_tts


def list_groups(event, possible_replies, tip=None):
    saved_groups = event['state']['user'].get('saved_groups')
    reply = random.choice(possible_replies["GROUP"]["LIST"])
    output_text = reply
    output_tts = reply
    if saved_groups:
        if len(saved_groups) > 0:
            output_text = "На данный момент сохранены следующие группы:\n"
            output_tts = output_text
            for i, saved_group in enumerate(event['state']['user']['saved_groups']):
                output_text += f"Номер {i + 1}: {saved_group['group']} ({saved_group['faculty']})\n"
                output_tts += f"Номер {i + 1}: {' '.join(saved_group['group'])} ({' '.join(saved_group['faculty'])}). "
            if tip:
                random_tip = random.choice(possible_replies['TIP'])
                output_text += random_tip
                output_tts += random_tip
    return output_text, output_tts


def remove_group(event, response_json, index):
    _, g = event['state']['user']['saved_groups'][index - 1].values()
    output_text = f"Группа {g} удалена"
    output_tts = f"Группа {' '.join(g)} удалена"
    del event['state']['user']['saved_groups'][index - 1]
    response_json['user_state_update']['saved_groups'] = event['state']['user']['saved_groups']
    return output_text, output_tts


def remove_group_options(event, response_json, possible_replies):
    (output_text, output_tts) = list_groups(event, possible_replies)
    if len(event['state']['user']['saved_groups']) > 0:
        response_json['user_state_update']['intent_remove'] = True
        reply = random.choice(possible_replies["GROUP"]["REMOVE_OPTIONS"])
        output_text += reply
        output_tts += reply
        for i in range(len(event['state']['user']['saved_groups'])):
            response_json['response']['buttons'].append({'title': str(i + 1), "hide": True})
    return output_text, output_tts


def reset_settings(event, response_json, sp, possible_reset):
    response_json['session_state'] = None
    user_settings = event['state'].get('user')
    if user_settings:
        for k in user_settings.keys():
            response_json['user_state_update'][k] = None
    response_json['application_state'] = {}
    sp.set_faculty(None)
    sp.set_group(None)
    reply = random.choice(possible_reset)
    output_text = reply
    output_tts = reply
    return output_text, output_tts


def gather_group(event, response_json, faculty, group, sp, rv, possible_requests, possible_replies):
    answer = event['request']['original_utterance'].lower()

    if group:
        if event['session']['new']:
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
            tip = random.choice(possible_replies['TIP'])
            output_text += tip
            output_tts += tip
        else:
            if any([list_request in answer for list_request in possible_requests['LIST']]):
                (output_text, output_tts) = list_groups(event, possible_replies, tip=True)
            elif any([save_request in answer for save_request in possible_requests['SAVE']]):
                (output_text, output_tts) = save_group(event, response_json)
            elif any([remove_request in answer for remove_request in possible_requests['REMOVE']]):
                (output_text, output_tts) = remove_group_options(event, response_json, possible_replies)
            else:
                (output_text, output_tts) = gather_date(event, response_json, sp, possible_replies)
    else:
        possible_group = group_recognition(event['request']['nlu']['tokens'])
        group_search = rv.validate_group(faculty, possible_group)
        if group_search == 0:
            reply = random.choice(possible_replies['GROUP_NOT_FOUND']["NO_MATCHES"])
            output_text = reply
            output_tts = reply
        elif group_search == 1:
            sp.set_group(possible_group)
            response_json['application_state']['group'] = possible_group
            (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
            tip = random.choice(possible_replies['TIP'])
            output_text += tip
            output_tts += tip
        elif group_search == -1:
            output_text = ""
            output_tts = ""
        else:
            reply = random.choice(possible_replies["GROUP_NOT_FOUND"]["TOO_MANY_FOUND"])
            output_text = reply
            output_tts = reply
    return output_text, output_tts


def gather_info(event, response_json, teacher, faculty, group, sp, possible_requests, possible_replies):
    rv = request_validation.RequestValidator()
    answer = event['request']['original_utterance'].lower()
    if any([stop_request in answer for stop_request in possible_requests['STOP']]):
        response_json['response']['end_session'] = True
        reply = random.choice(possible_replies['STOP'])
        output_text, output_tts = reply, reply
    elif any([help_request in answer for help_request in possible_requests['HELP']]):
        reply = random.choice(possible_replies['HELP'])
        output_text, output_tts = reply, reply
    elif event['state']['user'].get('intent_remove'):
        possible_index = event['request']['nlu']['entities']
        index = -1
        for pi in possible_index:
            if pi['type'] == "YANDEX.NUMBER":
                index = int(pi['value'])
                break
        if index != -1:
            (output_text, output_tts) = remove_group(event, response_json, index)
        else:
            (output_text, output_tts) = "Группа с таким номером не найдена", "Группа с таким номером не найдена"
        response_json['user_state_update']['intent_remove'] = False
    elif any([reset_request in answer for reset_request in possible_requests['RESET']]):
        (output_text, output_tts) = reset_settings(event, response_json, sp, possible_replies["RESET"])
    elif teacher:
        sp.set_teacher(teacher)
        if answer == 'смена преподавателя':
            sp.set_teacher(None)
            response_json['application_state']['teacher'] = None
            output_text = "Назовите имя преподавателя."
            output_tts = "Назовите имя преподавателя."
        else:
            (output_text, output_tts) = gather_date(event, response_json, sp, possible_replies)
    elif len([x for x in event['request']['nlu']['entities'] if x['type'] == "YANDEX.FIO"]) > 0:
        (output_text, output_tts) = "", ""
        possible_fio = event['request']['nlu']['entities']
        possible_teacher = ""
        for pf in possible_fio:
            if pf['type'] == "YANDEX.FIO":
                possible_teacher = teacher_recognition(pf['value'])
                break
        if possible_teacher != "":
            found = rv.validate_teacher(possible_teacher)
            if found == 1:
                sp.set_teacher(possible_teacher)
                (output_text, output_tts) = schedule_to_speech.translate(sp.get_schedule())
            elif found > 1:
                (output_text,
                 output_tts) = "Слишком много совпадений, уточните запрос", "Слишком много совпадений, уточните запрос"
            else:
                (output_text, output_tts) = "Преподаватель не найден", "Преподаватель не найден"
    elif faculty:
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
            faculty_buttons(sp, response_json)
        else:
            (output_text, output_tts) = gather_group(event, response_json, faculty, group, sp, rv, possible_requests,
                                                     possible_replies)
    elif rv.validate_faculty(answer):
        response_json['application_state']['faculty'] = sp.ABBR_CONVERSION[answer] if sp.set_faculty(answer) else \
            sp.NAME_ABBR[answer]
        output_text = "И номер группы."
        output_tts = "И номер группы."
    elif answer == "":
        output_text = ""
        output_tts = ""
        faculty_buttons(sp, response_json)
    else:
        output_text = "Ой, я такой институт не знаю, попробуйте еще раз."
        output_tts = "Ой, я такой институт не знаю, попробуйте еще раз."
        faculty_buttons(sp, response_json)
    return output_text, output_tts


def handler(event, context, requests="requests.yaml", replies="replies.yaml"):
    teacher = event['state']['application'].get('teacher')
    faculty = event['state']['application'].get('faculty')
    group = event['state']['application'].get('group')
    sp = schedule_parser.ScheduleParser(teacher, faculty, group)
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
        output_text, output_tts = gather_info(event, response_json, teacher, faculty, group, sp, possible_requests,
                                              possible_replies)
        response_json['response']['text'] += output_text
        response_json['response']['tts'] += output_tts
        return json.dumps(response_json)
