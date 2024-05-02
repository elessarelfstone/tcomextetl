from datetime import datetime
from tcomextetl.common.dates import dates_between
from tcomextetl.common.utils import dict_keys_to_snake_case
from tcomextetl.extract.api_requests import ApiRequests
from collections import deque
from time import sleep

from requests.exceptions import ReadTimeout


class CloudPaymentsParser(ApiRequests):
    @property
    def page(self):
        pass

    def __init__(self, url, dates, **kwargs):
        super(CloudPaymentsParser, self).__init__(**kwargs)
        self.url = url
        self._total = 0
        self.entity = 'Model'
        self._dates = deque(dates_between(*dates))

    def parse(self):
        data = self._raw.get(self.entity)
        formatted = [dict_keys_to_snake_case(d) for d in data]
        return formatted

    @property
    def total(self):
        return self._total

    @property
    def size(self):
        return 100

    @property
    def next_page_params(self):
        params = self.params

        if self._from:
            params['Date'] = self._from
        return params

    def load(self, params):
        r = self.session.request('POST', self.url, params=params, auth=self.auth, timeout=self.timeout)
        return r.json()

    def __iter__(self):

        self._start_date = datetime.now()

        self._from = self._dates.popleft()

        while self._from:
            try:
                self._raw = self.load(self.next_page_params)
                data = self.parse()
                self._parsed_count += len(data)
                self._end_date = datetime.now()
                if self._dates:
                    self._from = self._dates.popleft()
                else:
                    self._from = None
                yield data
            except ReadTimeout:
                sleep(self.timeout)
