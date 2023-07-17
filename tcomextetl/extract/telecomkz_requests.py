from time import sleep
from tcomextetl.extract.http_requests import HttpRequest
import logging


class TelecomkzYandexMetricsRequests(HttpRequest):

    def __init__(self, url, **kwargs):
        super(TelecomkzYandexMetricsRequests, self).__init__(**kwargs)
        self.url = url

    def load(self, params):

        r = self.request(self.url, params=params)

        while r.status_code == 202:
            sleep(self.timeout_ban)
            r = self.request(self.url, params=params)

        if r.status_code == 200:
            return r.content
        else:
            r.raise_for_status()



