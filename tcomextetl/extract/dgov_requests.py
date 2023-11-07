import re
from collections import deque
from datetime import date, datetime
from math import floor
from time import sleep

from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.extract.http_requests import HttpRequest

from settings import DATAGOV_TOKEN

host = 'https://data.egov.kz'
rep_page_tmpl = 'datasets/view?index={}'
data_page_tmpl = '/api/v4/{}/{}?apiKey={}'
detail_page_tmpl = '/api/detailed/{}/{}?apiKey={}'
meta_page_tmpl = '/meta/{}/{}'


class DgovParser(HttpRequest):
    def __init__(self, rep_name, rep_ver=None, parsed_chunks=None,
                 chunk_size=10000, **kwargs):

        super(DgovParser, self).__init__(**kwargs)
        self.rep_name = rep_name
        self.rep_ver = rep_ver
        self.chunk_size = chunk_size

        self._from = 1
        self._raw = self.load(url=self.detailed_url)
        self._parsed_count = 0
        self._query = None

        _chunks = self._compute_chunks()
        if parsed_chunks:
            self._chunks = [ch for ch in _chunks if str(ch) not in parsed_chunks]
            self._parsed_count = len(parsed_chunks) * chunk_size
        else:
            self._chunks = _chunks

        self._chunks = deque(self._chunks)

    def _compute_chunks(self):
        cnt, rem = divmod(self.total, self.chunk_size)
        if rem:
            cnt += 1

        # _chunks = []
        # for i in range(cnt):
        #     if i == 0:

        return [i * self.chunk_size + 1 for i in range(cnt)]

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
    def curr_chunk(self):
        return str(self._from)

    @property
    def query(self):

        q = '"from":%s,"size":%s' % (self._from, self.chunk_size)

        if self._from == 1:
            q = '"from":%s,"size":%s' % (0, self.chunk_size + 1)
        if self.params:
            params = self.params
            q += ', "query":{"range":{"modified":{"gte":"%s","lt":"%s"}}}' % (params['from'], params['to'])

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

    @property
    def status_percent(self):
        if self.total != 0:
            p = floor((self._parsed_count * 100) / self.total)
        else:
            p = 100
        s = f'Total: {self.total}. Parsed: {self._parsed_count}. '
        s += f'Chunk: {self._from}-{self._from + self.chunk_size - 1} ' + '\n'
        if self.params:
            p = self.params
            f = p['from']
            t = p['to']
            s += f'From: {f} to: {t}'
        return s, p

    @property
    def stat(self):
        return {"parsed": self._parsed_count}

    def __iter__(self):
        while self._chunks:
            self._from = self._chunks.popleft()
            self._raw = self.load()
            data = self.parse()
            self._parsed_count += len(data)
            yield data


