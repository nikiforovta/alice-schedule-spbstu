import datetime

import requests
from fuzzywuzzy import fuzz


class ScheduleParser:
    FACULTY_LIST = []
    NAME_ABBR = {}
    ABBR_CONVERSION = {}

    def __init__(self, faculty=None, group=None):
        self.faculty = None
        self.group = None
        self.session = requests.Session()
        self.FACULTY_LIST = self.get_faculties()
        for item in self.FACULTY_LIST:
            self.NAME_ABBR[item['name'].lower()] = item['abbr'].lower()
            self.ABBR_CONVERSION[item['abbr'].lower()] = item['abbr']
        if faculty is not None:
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

    def set_faculty_by_id(self, faculty_id):
        self.faculty = faculty_id
        pass

    def set_group(self, group):
        GROUP_DICT = self.get_groups()
        self.group = next((item['id'] for item in GROUP_DICT if item['name'] == group), None) if GROUP_DICT else None

    def get_info(self, url):
        search = f"https://ruz.spbstu.ru/api/v1/ruz/{url}"
        return self.session.get(search).json()

    def get_faculties(self):
        faculties = self.get_info('faculties')
        return faculties['faculties']

    def find_groups(self, group):
        groups = self.get_info(f'search/groups?q={group}')
        return groups['groups']

    def get_groups(self, faculty=None):
        if self.faculty:
            groups = self.get_info(f'faculties/{self.faculty}/groups')
            return groups['groups']
        elif faculty:
            groups = self.get_info(f'faculties/{faculty}/groups')
            return groups['groups']
        return None

    def find_group(self, faculty=None, type=None, level=None, spec=None, group_number=None, degree=None):
        if faculty and degree:
            groups = self.get_groups(faculty['value'])
            degree_list = ['bachelor', 'master']
            degree = degree_list.index(degree['value'])
        else:
            return None
        for group in groups:
            group_spec = ' '.join(group['spec'].split(" ")[1:]).lower()
            if group['level'] == level['value'] and group['type'] == type['value'] \
                    and fuzz.token_sort_ratio(group_spec, spec['value']) > 75 \
                    and group['name'][-1] == str(group_number['value']) and group['kind'] == degree:
                return group
        return None

    def compact_day(self, schedule_day):
        if schedule_day:
            compact_day = schedule_day
            lessons = compact_day.get('lessons')
            for i in range(len(lessons)):
                lessons[i].pop("subject_short", None)
                lessons[i].pop("type", None)
                lessons[i].pop("additional_info", None)
                lessons[i].pop("parity", None)
                lessons[i]['typeObj'].pop("id", None)
                lessons[i]['typeObj'].pop("abbr", None)
                lessons[i].pop("groups", None)
                teachers = lessons[i].get('teachers')
                if teachers:
                    for j in range(len(teachers)):
                        lessons[i]['teachers'][j] = teachers[j].get('full_name')
                auditories = lessons[i].get('auditories')
                if auditories:
                    for k in range(len(auditories)):
                        lessons[i]['auditories'][k].pop("id", None)
                        lessons[i]['auditories'][k]['building'].pop("id", None)
                        lessons[i]['auditories'][k]['building'].pop("abbr", None)
                        lessons[i]['auditories'][k]['building'].pop("address", None)
                lessons[i].pop("webinar_url", None)
                lessons[i].pop("lms_url", None)
            return compact_day
        return schedule_day

    def compact_week(self, schedule_week):
        compact_week = schedule_week
        for i in range(len(compact_week)):
            compact_week[i] = self.compact_day(schedule_week[i])
        return compact_week

    def get_schedule(self, date=datetime.datetime.now().strftime("%Y-%m-%d")):
        search = f'scheduler/{self.group}'
        search += f'?date={date}'
        schedule = self.get_info(search)
        return self.compact_day(next((item for item in schedule['days'] if item['date'] == date), None))

    def get_schedule_week(self):
        return self.get_info(f'scheduler/{self.group}')['days']
