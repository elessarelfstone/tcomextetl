from tcomextetl.extract.api_requests import ApiRequests
from tcomextetl.common.utils import flatten_dict, clean


class InfobipRestApiParser(ApiRequests):

    def __init__(self, url, entity, **kwargs):
        super(InfobipRestApiParser, self).__init__(**kwargs)
        self.url = url
        self.entity = entity

    @property
    def total(self):
        pagination = self._raw.get('pagination')
        return pagination['totalItems']

    @property
    def page(self):
        pagination = self._raw.get('pagination')
        return pagination['page']

    @property
    def size(self):
        pagination = self._raw.get('pagination')
        return pagination['limit']

    def load(self, params):
        r = self.request(self.url, params=params)
        return r.json()

    def parse(self):

        data = self._raw.get(self.entity)

        if data is None:
            return []

        normalized_data = [flatten_dict(d) for d in data]

        return [clean(d) for d in normalized_data if '_' not in d.keys()]

    @property
    def next_page_params(self):
        params = self.params

        if self._raw is None:
            return params

        if self._raw[self.entity]:
            params['page'] = self.page + 1

            # prevent next request
            if ((self.page + 1) * self.size) >= self.total:
                params = {}

        else:
            params = {}

        return params


