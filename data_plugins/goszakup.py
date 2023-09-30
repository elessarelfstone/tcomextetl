from collections.abc import Iterator
from pathlib import Path
from time import sleep


from data_plugins.base import BaseDataPlugin, HttpRequest, ExternalSourceError, FlattenedDict


class GoszakupDataPlugin(BaseDataPlugin, HttpRequest):

    def __init__(self, context):
        super(GoszakupDataPlugin, self).__init__(context)
        self._url = self.context.url
        self._entity = self.context.entity
        self._gql = self.context.gql
        self.last_id = None
        self._flatten = FlattenedDict()

        super(HttpRequest, self).__init__(
            **self.context.request
        )

    @property
    def _last_id(self) -> int:
        e = self._raw.get('extensions')
        return e['pageInfo']['lastId']

    @property
    def _page(self):
        e = self._raw.get('extensions')
        return e['pageInfo']['hasNextPage']

    def _qraphql(self) -> str:
        name = self._context['name']
        gql_fpath = Path(__file__).parent / 'misc' / 'gql' / f'{name}.gql'
        return gql_fpath.read_text()

    def _load(self, params):

        variables = params

        if self._raw:
            variables['after'] = self._last_id

        payload = {
            'query': self._qraphql(),
            'variables': variables
        }

        r = self.request(
            self._url,
            params=params,
            json=payload
        )

        return r.json()

    def _parse(self) -> list[dict]:

        # handle goszakup internal errors
        errors = self._raw.get('errors')
        if errors:
            raise ExternalSourceError(errors[0]['message'])

        data = self._raw['data'][self._entity]

        if data is None:
            return []

        return [self._flatten(d) for d in data]

    @property
    def _next_page_params(self):

        params = self.params
        if self._raw is None:
            return params

        if self._page:
            params['after'] = self.last_id
        else:
            params = {}

        return params

    def data(self, meta: dict | None = None) -> Iterator[list[dict]]:

        while self._next_page_params:
            self._raw = self._load(self._next_page_params)
            data = self._parse()
            yield data
            sleep(2)

    def stat(self) -> dict:
        return {}

    def progress_status(self) -> tuple[int, str]:
        return 0, 'sasad'
