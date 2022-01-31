import datetime

from . import schedule_parser


class RequestValidator:
    FACULTIES_LIST = []
    sp = schedule_parser.ScheduleParser()

    def __init__(self):
        for item in self.sp.FACULTY_DICT:
            self.FACULTIES_LIST.append(item["name"].lower())
            self.FACULTIES_LIST.append(item["abbr"].lower())

    def validate_faculty(self, faculty):
        return True if faculty in self.FACULTIES_LIST else False

    def validate_group(self, faculty, group):
        groups = self.sp.find_groups(group)
        group_match = 0
        for group in groups:
            if group['faculty']['name'].lower() == faculty or group['faculty']['abbr'].lower() == faculty:
                group_match += 1
        if group_match == 0:
            return "не знаю такой"
        if group_match == 1:
            return "группа найдена"
        else:
            return "уточните запрос"

    def validate_teacher(self, teacher):
        pass

    def validate_date(self, date):
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
