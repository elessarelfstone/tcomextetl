from math import floor
from time import sleep

from tcomextetl.extract.http_requests import HttpRequest
from abc import ABC, abstractmethod


class ApiRequests(ABC, HttpRequest):

    def __init__(self, **kwargs):
        super(ApiRequests, self).__init__(**kwargs)
        self._raw = None
        self._page = None
        self._parsed_count = 0

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
    def stat(self):
        return {'total': self.total, 'parsed': self._parsed_count,
                'page_params': self.next_page_params}

    @property
    def status_percent(self):
        if self.total == 0:
            p = 0
        else:
            p = floor((self._parsed_count * 100) / self.total)
        return f'Total: {self.total}. Parsed: {self._parsed_count}', p

    def __iter__(self):

        while self.next_page_params:
            self._raw = self.load(self.next_page_params)
            data = self.parse()
            self._parsed_count += len(data)
            yield data
            sleep(self.timeout)
