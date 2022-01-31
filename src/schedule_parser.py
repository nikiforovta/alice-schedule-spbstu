import json
import re

import requests
from bs4 import BeautifulSoup


class ScheduleParser:
    FACULTY_DICT = None

    def __init__(self, faculty=None, group=None):
        self.session = requests.Session()
        self.FACULTY_DICT = self.get_faculties()
        if faculty is not None and group is not None:
            self.faculty = next(item for item in self.FACULTY_DICT if item["abbr"] == faculty)['id']
            GROUP_DICT = self.get_groups(self.faculty)
            self.group = next(item for item in GROUP_DICT if item['name'] == group)['id']

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

    def get_groups(self, faculty):
        groups = self.get_info(f'https://ruz.spbstu.ru/faculty/{faculty}/groups/')
        return groups['groups']['data'][str(faculty)]

    def get_schedule(self, date):
        if date is None:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}')
        else:
            schedule = self.get_info(f'https://ruz.spbstu.ru/faculty/{self.faculty}/groups/{self.group}?date={date}')
        return schedule['lessons']['data'][str(self.group)]
