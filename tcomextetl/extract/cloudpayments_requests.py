from tcomextetl.common.utils import dict_keys_to_snake_case
from tcomextetl.extract.api_requests import ApiRequests


class CloudPaymentsParser(ApiRequests):
    @property
    def page(self):
        pass

    def __init__(self, url, **kwargs):
        super(CloudPaymentsParser, self).__init__(**kwargs)
        self.url = url
        self._queue = None
        self._total = 0
        self.entity = 'Model'
        self.next_page = 0

    def parse(self):
        data = self._raw.get(self.entity)
        formatted = [dict_keys_to_snake_case(d) for d in data]
        self.next_page += 1
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
        if self._raw is None:
            return params

        if self._raw[self.entity]:
            params['PageNumber'] = self.next_page + 1
        else:
            params = {}
        return params

    def load(self, params):
        r = self.session.request('POST', self.url, params=params, auth=self.auth, timeout=self.timeout)
        return r.json()
