import json

import requests
from bs4 import BeautifulSoup


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
        self.set_teacher(teacher)
        self.set_faculty(faculty)
        self.set_group(group)

    def set_faculty(self, faculty):
        for item in self.FACULTY_LIST:
            if faculty == item['abbr']:
                self.faculty = item['id']
                return True
        return False

    def set_group(self, group):
        GROUP_DICT = self.get_groups()
        self.group = next((item['id'] for item in GROUP_DICT if item['name'] == group), None) if GROUP_DICT else None

    def set_teacher(self, teacher):
        self.teacher = None
        if teacher:
            TEACHERS_DICT = self.find_teachers(teacher)
            self.teacher = TEACHERS_DICT[0]['id'] if TEACHERS_DICT else None

    def get_info(self, url):
        soup = BeautifulSoup(self.session.get(url).text, 'lxml')
        for script in soup.select('body > script:nth-child(3)'):
            return json.loads(script.text[32:-3])

    def get_faculties(self):
        faculties = self.get_info('https://ruz.spbstu.ru/')
        return faculties['faculties']['data']

    def find_groups(self, group):
        group = '%2F'.join(group.split('/'))
        result = self.get_info(f'https://ruz.spbstu.ru/search/groups?q={group}')
        return result['searchGroup']['data']

    def find_teachers(self, teacher):
        result = self.get_info(f'https://ruz.spbstu.ru/search/teacher?q={teacher}')
        return result['searchTeacher']['data']

    def get_groups(self):
        if self.faculty:
            groups = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/')
            return groups['groups']['data'][str(self.faculty)]
        return None

    def get_schedule(self, date=None):
        if self.teacher is None:
            if date is None:
                schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}')
            else:
                schedule = self.get_info(
                    f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}?date={date}')
            return schedule['lessons']['data'][str(self.group)]
        else:
            if date is None:
                schedule = self.get_info(f'https://ruz.spbstu.ru/teachers/{self.teacher}')
            else:
                schedule = self.get_info(f'https://ruz.spbstu.ru/teachers/{self.teacher}?date={date}')
            return schedule['teacherSchedule']['data'][str(self.teacher)]
