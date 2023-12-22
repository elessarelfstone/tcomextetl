import json

import requests

from tcomextetl.extract.http_requests import HttpRequest


class TvPlusParser(HttpRequest):

    def __init__(self, url, **kwargs):
        super(TvPlusParser, self).__init__(**kwargs)
        self.url = url

    @property
    def stat(self) -> dict:
        return {}

    def load(self, params=None):

        r = self.request(self.url, params=params)
        return r.json()


class TvPlusProgramsParser(HttpRequest):

    def __init__(self, url, **kwargs):
        super(TvPlusProgramsParser, self).__init__(**kwargs)
        self.url = url

    @property
    def stat(self) -> dict:
        return {}

    def load(self, params=None):
        r = self.request(self.url, params=params)
        return r.text