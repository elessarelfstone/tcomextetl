from abc import ABC, abstractmethod
from datetime import datetime
from math import floor
from time import sleep

import humanize
from requests.exceptions import ReadTimeout

from tcomextetl.common.dates import DEFAULT_DATETIME_FORMAT
from tcomextetl.extract.http_requests import HttpRequest


class ApiRequests(ABC, HttpRequest):

    def __init__(self, **kwargs):
        super(ApiRequests, self).__init__(**kwargs)
        self._raw = None
        self._page = None
        self._parsed_count = 0
        self._start_date: datetime = datetime.now()
        self._end_date: datetime = datetime.now()
        self._max_retries = 5

    def set_parsed_count(self, count: int):
        self._parsed_count = count

    @property
    @abstractmethod
    def total(self):
        pass

    @property
    @abstractmethod
    def page(self):
        pass

    @property
    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def load(self, params):
        pass

    @abstractmethod
    def parse(self):
        pass

    @property
    @abstractmethod
    def next_page_params(self):
        pass

    @property
    def stat(self) -> dict:
        return {
            'start': self._start_date.strftime(DEFAULT_DATETIME_FORMAT),
            'end': self._end_date.strftime(DEFAULT_DATETIME_FORMAT),
            'duration': humanize.precisedelta(self._end_date - self._start_date),
            'total': self.total,
            'parsed': self._parsed_count,
            'page_params': self.next_page_params
        }

    @property
    def status_percent(self):
        if self.total == 0:
            p = 0
        else:
            p = floor((self._parsed_count * 100) / self.total)
        return f'Total: {self.total}. Parsed: {self._parsed_count}', p

    def __iter__(self):

        self._start_date = datetime.now()
        exp_backoff = self.timeout
        while self.next_page_params:
            for _ in range(self._max_retries):
                try:
                    self._raw = self.load(self.next_page_params)
                    data = self.parse()
                    self._parsed_count += len(data)
                    self._end_date = datetime.now()
                    yield data
                    if self.timeout_ban:
                        sleep(self.timeout_ban)
                    break
                except ReadTimeout:
                    sleep(exp_backoff)
                    exp_backoff *= 2
