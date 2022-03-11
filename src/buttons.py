def date_buttons(response_json):
    response_json['response']['buttons'].append({"title": "Вчера", "hide": True})
    response_json['response']['buttons'].append({"title": "Сегодня", "hide": True})
    response_json['response']['buttons'].append({"title": "Завтра", "hide": True})


def faculty_buttons(sp, response_json):
    for faculty in sp.FACULTY_LIST:
        response_json['response']['buttons'].append({"title": faculty["abbr"], "hide": True})
