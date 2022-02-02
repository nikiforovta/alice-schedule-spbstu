import json
import re

import requests
from bs4 import BeautifulSoup


class ScheduleParser:
    FACULTY_DICT = None

    def __init__(self, faculty=None, group=None):
        self.group = None
        self.faculty = None
        self.session = requests.Session()
        self.FACULTY_DICT = self.get_faculties()
        if faculty is not None and group is not None:
            self.set_faculty(faculty)
            self.set_group(group)

    def set_faculty(self, faculty):
        self.faculty = next((item['id'] for item in self.FACULTY_DICT if item["abbr"].lower() == faculty), None)

    def set_group(self, group):
        GROUP_DICT = self.get_groups()
        self.group = next((item['id'] for item in GROUP_DICT if item['name'] == group), None)

    def get_info(self, url):
        soup = BeautifulSoup(self.session.get(url, headers={'Accept-Encoding': 'identity'}).text, 'html.parser')
        for script in soup.find_all(string=re.compile('window.__INITIAL_STATE__')):
            return json.loads(script[33:-3])

    def get_faculties(self):
        faculties = self.get_info(f'https://ruz.spbstu.ru/')
        return faculties['faculties']['data']

    def find_groups(self, group):
        group = '%2F'.join(group.split('/'))
        result = self.get_info(f'https://ruz.spbstu.ru/search/groups?q={group}')
        return result['searchGroup']['data']

    def get_groups(self):
        groups = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/')
        return groups['groups']['data'][str(self.faculty)]

    def get_schedule(self, date=None):
        if date is None:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}')
        else:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}?date={date}')
        return schedule['lessons']['data'][str(self.group)]
