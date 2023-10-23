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


class TelecomkzYandexMetricsLogsRequests(HttpRequest):

    def __init__(self, host, **kwargs):
        super(TelecomkzYandexMetricsLogsRequests, self).__init__(**kwargs)
        self.host = host

    def load(self, counter_id, data):

        # make order
        order_url = f'{self.host}/management/v1/counter/{counter_id}/logrequests'
        r = self.request(order_url, data=data)
        request_id = r.json()['log_request']['request_id']

        # check order
        check_url = f'{self.host}/management/v1/counter/{counter_id}/logrequest/{request_id}'
        r = self.request(check_url)
        ready = False
        while (not r.status_code == 200) or (not r.json()['log_request']['status'] == 'processed'):
            sleep(self.timeout_ban)
            r = self.request(check_url)

            if r.status_code >= 400:
                r.raise_for_status()

        parts = r.json()['log_request']['parts']

        # requests to retrieve data
        data = []
        for p in range(len(parts)):
            data_url = f'{self.host}/management/v1/counter/{counter_id}/logrequest/{request_id}/part/{str(p)}/download'
            r = self.request(data_url)
            data.append(r.text)

        return data
