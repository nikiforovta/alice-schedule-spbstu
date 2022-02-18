import schedule_parser


class RequestValidator:
    FACULTIES_LIST = []
    sp = schedule_parser.ScheduleParser()

    def __init__(self):
        for item in self.sp.FACULTY_LIST:
            self.FACULTIES_LIST.append(item["name"].lower())
            self.FACULTIES_LIST.append(item["abbr"].lower())

    def validate_faculty(self, faculty):
        return True if faculty in self.FACULTIES_LIST else False

    def validate_group(self, faculty, group):
        groups = self.sp.find_groups(group)
        group_match = sum(1 for group in groups if group['faculty']['name'].lower() == faculty
                          or group["faculty"]['abbr'].lower() == faculty)
        return group_match
