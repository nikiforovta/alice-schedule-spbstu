import random
import threading


def update_schedule(event, response_json, sp):
    saved_groups = event['state']['user'].get('saved_groups')
    for i in range(len(saved_groups)):
        sp.set_faculty(saved_groups[i]['faculty'])
        sp.set_group(saved_groups[i]['group'])
        schedule = sp.get_schedule_week()
        saved_schedule = saved_groups[i].get('schedule')
        if schedule != saved_schedule and len(schedule) > len(saved_schedule):
            response_json['user_state_update']['saved_groups'][i]['schedule'] = schedule


def save_schedule(response_json, sp):
    for i in range(len(response_json['user_state_update']['saved_groups'])):
        response_json['user_state_update']['saved_groups'][i]['schedule'] = sp.compact_week(sp.get_schedule_week())


def save_group(event, response_json, sp):
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
    threading.Thread(target=save_schedule, args=(response_json, sp)).run()
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
