from time import sleep
from urllib.parse import urlparse
from urllib.parse import parse_qsl

from tcomextetl.extract.api_requests import ApiRequests


def unnest(wrapper_entity: str, data: list):
    unnested = []
    for wrapper in data:
        items = wrapper[wrapper_entity]
        unnested.extend(items)

    return unnested


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
        params = self.params

        if self._raw is None:
            return params

        # print(params)
        query = urlparse(self.page).query
        query_params = dict(parse_qsl(query))
        params.update(query_params)
        return params


class GoszakupGraphQLApiParser(ApiRequests):

    def __init__(self, url, entity, anchor_key, **kwargs):
        super(GoszakupGraphQLApiParser, self).__init__(**kwargs)
        self.url = url
        self.entity = entity
        self.anchor_key = anchor_key

    @property
    def total(self):
        ext = self._raw.get('extensions')
        return ext['pageInfo']['totalCount']

    @property
    def page(self):
        ext = self._raw.get('extensions')
        return ext['pageInfo']['hasNextPage']

    @property
    def size(self):
        ext = self._raw.get('extensions')
        return ext['pageInfo']['limitPage']

    @property
    def last_id(self):
        ext = self._raw.get('extensions')
        return ext['pageInfo']['lastId']

    def load(self, params):
        r = self.request(self.url, params=params, data=)
        return r.json()

    def parse(self):
        entity, nested_wrapper = self.entity, None
        if '_' in self.entity:
            entity, nested_wrapper = self.entity.split('_')
        print(self._raw)
        data = self._raw['data'][entity]

        if nested_wrapper:
            data = unnest(nested_wrapper, data)

        return data

    @property
    def next_page_params(self):

        params = self.params
        if self._raw is None:
            return params

        if self.page:
            params['after'] = self.last_id
        else:
            params = {}

        return params