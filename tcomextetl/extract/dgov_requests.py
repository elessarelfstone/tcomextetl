import re
from collections import deque
from datetime import date, datetime

from tcomextetl.extract.http_requests import HttpRequest

from settings import DATAGOV_TOKEN

host = 'https://data.egov.kz'
rep_page_tmpl = 'datasets/view?index={}'
data_page_tmpl = '/api/v4/{}/{}?apiKey={}'
detail_page_tmpl = '/api/detailed/{}/{}?apiKey={}'
meta_page_tmpl = '/meta/{}/{}'

headers = {'user-agent': 'Apache-HttpClient/4.1.1 (java 1.5)'}


class DgovParser(HttpRequest):
    def __init__(self, rep_name, rep_ver=None, parsed_chunks=None, chunk_size=10000,
                 timeout=2, **kwargs):

        super(DgovParser, self).__init__(**kwargs)
        self.rep_name = rep_name
        self.rep_ver = rep_ver
        self.chunk_size = chunk_size

        self._raw = self.load(url=self.detailed_url)
        self._from = 1
        self._query = None

        _chunks = deque(self._compute_chunks())
        if parsed_chunks:
            self._chunks = [ch for ch in _chunks if ch not in parsed_chunks]
        else:
            self._chunks = _chunks

    def _compute_chunks(self):
        chunks, rem = divmod(self.total, self.chunk_size)
        if rem:
            chunks += 1

        return [i * self.chunk_size + 1 for i in range(chunks)]

    @property
    def data_page_uri(self):
        v = self.rep_ver if self.rep_ver else ''
        uri = f'/api/v4/{self.rep_name}/{v}?apiKey={DATAGOV_TOKEN}'
        return uri.replace('//', '/')

    @property
    def rep_page_uri(self):
        return f'datasets/view?index={self.rep_name}'

    @property
    def detail_page_uri(self):
        v = self.rep_ver if self.rep_ver else ''
        uri = f'/api/detailed/{self.rep_name}/{v}?apiKey={DATAGOV_TOKEN}'
        return uri.replace('/?', '?')

    @property
    def meta_page_uri(self):
        v = self.rep_ver if self.rep_ver else ''
        uri = f'/meta/{self.rep_name}/{v}'
        return uri.replace('//', '')

    @property
    def total(self):
        return self._raw['totalCount']

    @property
    def query(self):

        q = '"from":%s,"size":%s' % (self._from, self.chunk_size)
        p = self.params
        start = p.get('start')
        end = p.get('end')
        if start:
            start = datetime.strptime(start, '%Y-%m-%d').strftime('%Y-%m-%d %H:%M:%S')
            end = datetime.strptime(end, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            end = end.strftime('%Y-%m-%d %H:%M:%S')
            q += ', "query":{"range":{"modified":{"gte":"%s","lt":"%s"}}}' % (start, end)

        return '{%s}' % q

    @property
    def url(self):
        return f'{host}{self.detail_page_uri}&source={self.query}'

    @property
    def detailed_url(self):
        query = re.sub(pattern=r'(?<="size":)(\d+)', repl=r'1', string=self.query)
        return f'{host}{self.detail_page_uri}&source={query}'

    def request(self, url: str, data=None, json=None, params=None, stream=False):
        if data or json:
            method = 'POST'
        else:
            method = 'GET'

        return self.session.request(method, url, params=params,
                                    data=data, json=json, headers=self.headers,
                                    auth=self.auth, stream=stream,
                                    verify=self.verify_cert)

    def load(self, url=None):
        _url = self.url
        if url:
            _url = url
        r = self.request(_url)
        return r.json()

    def parse(self):
        return self._raw['data']

    def __iter__(self):
        while self._chunks:
            self._from = self._chunks.popleft()
            self._raw = self.load()
            data = self.parse()
            yield data[:3]




