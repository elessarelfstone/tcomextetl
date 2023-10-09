from tcomextetl.extract.api_requests import ApiRequests


def flatten_dict(d: dict) -> dict:
    """ """

    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                if name:
                    sep = '_'
                else:
                    sep = ''
                flatten(x[a], name + sep + a)
        elif type(x) is list:
            i = 0
            _x = [True if type(i) in [list, dict] else False for i in x]
            if all(_x):
                for a in x:
                    flatten(a, name + str(i) + '_')
                    i += 1
            else:
                out[name] = x
        else:
            out[name] = x

    flatten(d)

    return out


class SamrukParser(ApiRequests):
    def __init__(self, url, entity='content', **kwargs):
        super().__init__(**kwargs)

        self._url = url
        self.entity = entity
        self._params = self.params
        self.params = {}

    @property
    def total(self):
        return self._raw['totalElements']

    @property
    def page(self):
        return self._raw['number']

    @property
    def size(self):
        return self._raw['size']

    def load(self, params):

        key_value_pairs = []
        for key, value in self.next_page_params.items():
            key_value_pairs.append(f"{key}={value}")

        url = self._url + '?' + "&".join(key_value_pairs)

        r = self.request(url)
        return r.json()

    def parse(self):

        data = self._raw.get(self.entity)
        normalized_data = [flatten_dict(d) for d in data]

        return normalized_data

    @property
    def is_last(self):
        return self._raw['last']

    @property
    def next_page_params(self):
        params = self._params

        # is it first request
        if self._raw is None:
            return params

        if self._raw[self.entity]:
            params['page'] = self.page + 1

            # prevent next request
            if self.is_last:
                params = {}
        else:
            params = {}

        return params


class SamrukPlansRestApiParser(SamrukParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def page(self):
        return self._raw['number']

