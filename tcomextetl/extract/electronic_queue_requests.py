import json
from abc import ABC

import requests


from tcomextetl.extract.http_requests import HttpRequest
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import read_file, flatten_dict


class ElectronicQueueApiParser(HttpRequest):

    def __init__(self, url, data=None, **kwargs):
        super(ElectronicQueueApiParser, self).__init__(**kwargs)
        self.url = url
        self.data = data
        self._raw = None
        self._parsed_count = 0

    def load(self):
        r = requests.get(self.url, headers=self.headers, data=json.dumps(self.data))
        if r.status_code != 200:
            raise ExternalSourceError(f"Ошибка в запросе: {r.status_code}")
        return r.json()

    def set_parsed_count(self, count):
        self._parsed_count = count

    @property
    def status_percent(self):
        # Статус прогресса для статистики
        return self._parsed_count, len(self._raw) if self._raw else 0

    @property
    def stat(self):
        # Возвращаем статистику парсинга
        return {
            'parsed': self._parsed_count
        }
