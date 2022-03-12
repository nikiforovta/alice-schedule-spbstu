import random

import datetime_operations
import request_validation
import schedule_to_speech
from buttons import date_buttons, faculty_buttons
from group_operations import remove_group_options, save_group, list_groups, remove_group
from recognition import group_recognition, teacher_recognition


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
                (output_text, output_tts) = save_group(event, response_json, sp)
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
