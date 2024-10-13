import pandas as pd

from urllib.parse import urlparse
from urllib.parse import parse_qsl

from tenacity import retry, wait_fixed, stop_after_attempt

from tcomextetl.extract.api_requests import ApiRequests
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import read_file, flatten_dict, clean


def unnest(wrapper_entity: str, data: list):
    unnested = []

    # there are a few cases where
    # query has nested entity
    for wrapper in data:
        items = wrapper[wrapper_entity]
        unnested.extend(items)

    return unnested


def norm(d):
    df = pd.json_normalize(d, sep='')
    n = df.to_dict(orient='records')[0]
    return {k.lstrip('_'): v for k, v in n.items()}


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

    @retry(wait=wait_fixed(15), stop=stop_after_attempt(3))
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

        if not self.page:
            return {}

        # parse parameters for pagination
        query = urlparse(self.page).query
        query_params = dict(parse_qsl(query))

        params.update(query_params)
        return params


class GoszakupGraphQLApiParser(ApiRequests):

    def __init__(self, url, entity, gql_fpath, **kwargs):
        super(GoszakupGraphQLApiParser, self).__init__(**kwargs)
        self.url = url
        self.entity = entity
        self.graphql_script = read_file(gql_fpath)

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

        variables = params

        if self._raw:
            # pagination
            variables['after'] = self.last_id

        json = {'query': self.graphql_script, 'variables': variables}
        r = self.request(self.url, params=params, json=json)

        return r.json()

    def parse(self):

        # there are always 2 sections - data and extensions in response
        # check out if we got errors
        errors = self._raw.get('errors')
        if errors:
            raise ExternalSourceError(errors[0]['message'])

        data = self._raw['data'][self.entity]

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

        if self.page:
            params['after'] = self.last_id
        else:
            params = {}

        return params
