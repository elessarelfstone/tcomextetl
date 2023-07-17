import re
from collections import deque

from tcomextetl.common.utils import dict_keys_to_snake_case
from tcomextetl.extract.api_requests import ApiRequests


class CrmSensor(ApiRequests):

    def __init__(self, url, **kwargs):
        super(CrmSensor, self).__init__(**kwargs)
        self.url = url
        self._queue = None

    @property
    def total(self):
        return len(self._raw)

    @property
    def page(self):
        return 1

    def load(self, params):
        r = self.request(self.url, params=params)
        return r.json()

    @property
    def size(self):
        return self.params['limit']

    def parse(self):
        return None

    def _parse(self, d):

        # def to_snake_case(d):
        #     return {re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower(): value for (key, value) in d.items() if key != 'Data'}

        dicts = []
        base_d = {key: value for (key, value) in d.items() if key != 'Data'}
        questions = d['Data']
        for d in questions:

            _d = {**base_d, **d}
            dicts.append(dict_keys_to_snake_case(_d))

        return dicts

    @property
    def next_page_params(self):
        return {}

    def __iter__(self):

        queue = deque(self.load(self.params))

        while queue:
            d = queue.pop()
            yield self._parse(d)








