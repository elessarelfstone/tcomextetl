from tcomextetl.extract.api_requests import ApiRequests


class SamrukRestApiParser(ApiRequests):
    def __init__(self, url, entity='content', **kwargs):
        super().__init__(**kwargs)

        self.url = url
        self.entity = entity

    @property
    def total(self):
        return self._raw['totalElements']

    @property
    def page(self):
        return self._raw['page']

    @property
    def size(self):
        return self._raw['size']

    def load(self, params):
        r = self.request(self.url, params=params)
        return r.json()

    def parse(self):
        return self._raw.get(self.entity)

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
