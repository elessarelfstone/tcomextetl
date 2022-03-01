from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qsl

from tcomextetl.extract.api_requests import ApiRequests
from tcomextetl.common.csv import dict_to_csvrow


class GoszakupRestApiParser(ApiRequests):

    def __init__(self, url, **kwargs):
        super(GoszakupRestApiParser, self).__init__(**kwargs)
        self.url = url

    @property
    def total(self):
        return self._raw.get('total')

    @property
    def page(self):
        return self._raw.get('next_page')

    @property
    def size(self):
        return self._raw.get('size')

    def load(self, params):
        r = self.request(self.url, params=params)
        return r.json()

    def parse(self):
        return self._raw.get('items')

    @property
    def next_page_params(self):
        if self._raw is None:
            return {'page': 'next'}

        query = urlparse(self.page).query
        return dict(parse_qsl(query))
