import datetime

import requests


class ScheduleParser:
    FACULTY_LIST = []
    NAME_ABBR = {}
    ABBR_CONVERSION = {}

    def __init__(self, teacher=None, faculty=None, group=None):
        self.teacher = None
        self.faculty = None
        self.group = None
        self.session = requests.Session()
        self.FACULTY_LIST = self.get_faculties()
        for item in self.FACULTY_LIST:
            self.NAME_ABBR[item['name'].lower()] = item['abbr'].lower()
            self.ABBR_CONVERSION[item['abbr'].lower()] = item['abbr']
        if teacher is not None:
            self.set_teacher(teacher)
        elif faculty is not None:
            self.set_faculty(faculty)
            if group is not None:
                self.set_group(group)

    def set_faculty(self, faculty):
        for item in self.FACULTY_LIST:
            if faculty == item['abbr'].lower() or faculty == item['abbr']:
                self.faculty = item['id']
                return True
            elif faculty == item['name'].lower():
                self.faculty = item['id']
                return False
        return False

    def set_group(self, group):
        GROUP_DICT = self.get_groups()
        self.group = next((item['id'] for item in GROUP_DICT if item['name'] == group), None) if GROUP_DICT else None

    def set_teacher(self, teacher):
        self.teacher = None
        if teacher:
            teachers = self.find_teachers(teacher)
            self.teacher = teachers[0]['id'] if len(teachers) > 0 else None

    def get_info(self, url):
        search = f"https://ruz.spbstu.ru/api/v1/ruz/{url}"
        return self.session.get(search).json()

    def get_faculties(self):
        faculties = self.get_info('faculties')
        return faculties['faculties']

    def find_groups(self, group):
        groups = self.get_info(f'search/groups?q={group}')
        return groups['groups']

    def find_teachers(self, teacher):
        teachers = self.get_info(f'search/teachers?q={teacher}')
        return teachers['teachers']

    def get_groups(self):
        if self.faculty:
            groups = self.get_info(f'faculties/{self.faculty}/groups')
            return groups['groups']
        return None

    def get_schedule(self, date=datetime.datetime.now().strftime("%Y-%m-%d")):
        search = f'teachers/{self.teacher}/scheduler' if self.teacher else f'scheduler/{self.group}'
        search += f'?date={date}'
        schedule = self.get_info(search)
        return next((item for item in schedule['days'] if item['date'] == date), None)
