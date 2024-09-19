import time
import pandas as pd
import requests

from urllib.parse import urlparse
from urllib.parse import parse_qsl

from requests import ConnectTimeout

from tcomextetl.extract.api_requests import ApiRequests
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import read_file, flatten_dict, clean


class ShopTelecomKZApiParser(ApiRequests):

    def __init__(self, url, entity='data', **kwargs):
        super(ShopTelecomKZApiParser, self).__init__(**kwargs)
        self.url = url
        self.entity = entity

    @property
    def total(self):
        pagination = self._raw.get('pagination')
        return pagination['total']

    @property
    def page(self):
        pagination = self._raw.get('pagination')
        return pagination['next_page_url']

    @property
    def size(self):
        pagination = self._raw.get('pagination')
        return pagination['last_page']

    def load(self, params):
        r = requests.get(self.url, params=params, headers=self.headers)
        if r.status_code != 200:
            raise ExternalSourceError(f"Ошибка в запросе: {r.status_code}")
        return r.json()

    def parse(self):
        data = self._raw['data']

        if data is None:
            return []

        # level up nested data
        normalized_data = [flatten_dict(d) for d in data]

        #
        return [clean(d) for d in normalized_data if '_' not in d.keys()]

    @property
    def next_page_params(self):
        params = self.params
        if self._raw is None:
            return params
        if not self.page:
            return {}
        query = urlparse(self.page).query
        query_params = dict(parse_qsl(query))
        params.update(query_params)
        return params

