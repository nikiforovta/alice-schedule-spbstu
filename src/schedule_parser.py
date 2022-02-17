import json
import re

import requests
from bs4 import BeautifulSoup


class ScheduleParser:
    FACULTY_LIST = {}
    NAME_ABBR = {}

    def __init__(self, faculty=None, group=None):
        self.faculty = faculty
        self.group = group
        self.session = requests.Session()
        self.FACULTY_LIST = self.get_faculties()
        for item in self.FACULTY_LIST:
            self.NAME_ABBR[item['name'].lower()] = item['abbr'].lower()
        if faculty is not None and group is not None:
            self.set_faculty(faculty)
            self.set_group(group)

    def set_faculty(self, faculty):
        self.faculty = None
        for item in self.FACULTY_LIST:
            if faculty == item['abbr'].lower():
                self.faculty = item['id']
                return True
            elif faculty == item['name'].lower():
                self.faculty = item['id']
                return False

    def set_group(self, group):
        GROUP_DICT = self.get_groups()
        self.group = next((item['id'] for item in GROUP_DICT if item['name'] == group), None) if GROUP_DICT else None

    def get_info(self, url):
        soup = BeautifulSoup(self.session.get(url).text, 'lxml')
        for script in soup.select('body > script:nth-child(3)'):
            return json.loads(script.text[32:-3])

    def get_faculties(self):
        faculties = self.get_info(f'https://ruz.spbstu.ru/')
        return faculties['faculties']['data']

    def find_groups(self, group):
        group = '%2F'.join(group.split('/'))
        result = self.get_info(f'https://ruz.spbstu.ru/search/groups?q={group}')
        return result['searchGroup']['data']

    def get_groups(self):
        if self.faculty:
            groups = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/')
            return groups['groups']['data'][str(self.faculty)]
        return None

    def get_schedule(self, date=None):
        if date is None:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}')
        else:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}?date={date}')
        return schedule['lessons']['data'][str(self.group)]
