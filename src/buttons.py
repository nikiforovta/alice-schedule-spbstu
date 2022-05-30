import random


def date_buttons(response_json):
    response_json['response']['buttons'].append({"title": "Вчера", "hide": True})
    response_json['response']['buttons'].append({"title": "Сегодня", "hide": True})
    response_json['response']['buttons'].append({"title": "Завтра", "hide": True})


def faculty_buttons(sp, response_json):
    for faculty in sp.FACULTY_LIST:
        response_json['response']['buttons'].append({"title": faculty["abbr"], "hide": True})


def group_buttons(sp, response_json):
    groups = sp.get_groups(response_json['session_state']['group'])
    for _ in range(random.randint(3, 6)):
        response_json['response']['buttons'].append({"title": random.choice(groups)["name"], "hide": True})


def additional_buttons(response_json, possible_requests):
    response_json['response']['buttons'].append(
        {"title": random.choice(possible_requests['STOP']).capitalize(), "hide": True})
    response_json['response']['buttons'].append(
        {"title": random.choice(possible_requests['HELP']).capitalize(), "hide": True})
