from collections import Counter
from http.client import RemoteDisconnected
from json import dumps, loads
from xmltodict import parse
from xml.parsers.expat import ExpatError
from urllib3.exceptions import ProtocolError

from requests.exceptions import HTTPError, ConnectionError, ReadTimeout
from tenacity import retry, wait_fixed, stop_after_attempt

from tcomextetl.extract.http_requests import HttpRequest
from tcomextetl.common.exceptions import ExternalSourceError


class KgdGovKzSoapApiError(Exception):
    pass


class KgdGovKzSoapApiResponseError(Exception):
    pass


class KgdGovKzSoapApiNotAvailable(Exception):
    pass


class KgdGovKzSoapApiParser(HttpRequest):

    def __init__(self, url, request_form, **kwargs):
        super(KgdGovKzSoapApiParser, self).__init__(**kwargs)
        self.url = url
        self.request_form = request_form
        self._raw = None
        self._page = None
        self._parsed_cnt = 0
        self._stat_meta_info = Counter()
        # re - response error
        # se - service error(xml tag <error> in response)
        # ce - connection error(Http, Connection, etc)
        # s - success
        for s in ['re', 'se', 'ce', 's', 'p']:
            self._stat_meta_info.setdefault(s, 0)

        self._last_conn_errors_cnt = 0

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, val):
        self._raw = val

    @property
    def stat_meta_info(self):
        s = """
Response errors: {} - response that can't be represented as xml
Service errors: {} - internal KGD soap api errors(with codes)
Availability errors: {} - connection issues, http, too many requests, etc  
Successes: {} - successfully processed BINs
""".format(*self._stat_meta_info.values())
        return s

    @property
    def stat(self):
        stat = dict()
        stat['Parsed'] = self._parsed_cnt
        stat['Response errors'] = self._stat_meta_info['re']
        stat['Service errors'] = self._stat_meta_info['se']
        stat['Availability errors'] = self._stat_meta_info['ce']
        stat['Successes'] = self._stat_meta_info['s']
        return stat

    @property
    def is_server_up(self):
        if self._last_conn_errors_cnt > 10:
            return False

        return True

    @retry(wait=wait_fixed(15), stop=stop_after_attempt(3))
    def load(self, params):
        request_xml = self.request_form.format(*params.values())
        r = self.request(self.url, data=request_xml)
        return r.text

    def parse(self):

        if not self._raw:
            self._stat_meta_info['re'] += 1
            raise KgdGovKzSoapApiResponseError('Empty response')
        try:
            # parse xml to dict
            raw_json = loads(dumps(parse(self._raw)))
            answer = raw_json['answer']
        except (ExpatError, KeyError):
            self._stat_meta_info['re'] += 1
            raise KgdGovKzSoapApiResponseError('Not XML formatted')

        if answer and 'err' in answer.keys():
            errcode = answer['err']['@errorcode']
            raise KgdGovKzSoapApiError(f'Errorcode {errcode}')

        # we can get one payment as single dict, so we have wrap it in list
        payments = answer['payment'] if isinstance(answer['payment'], list) else [answer['payment']]

        data = []
        for d in payments:
            # skip payments without Summa
            if d['Summa']:
                # response doesn't contain BIN
                d['bin'] = answer['IIN_BIN']

            if d.get('Summa') is not None:
                data.append(d)

        return data

    def process_bin(self, _bin):
        params = {'bin': _bin, **self.params}
        try:
            self._raw = self.load(params)
            data = self.parse()
        except KgdGovKzSoapApiError:
            self._stat_meta_info['se'] += 1
            raise
        except (ConnectionError, ProtocolError, HTTPError,
                ReadTimeout, RemoteDisconnected):
            self._stat_meta_info['ce'] += 1
            self._last_conn_errors_cnt += 1
            raise KgdGovKzSoapApiNotAvailable
        except Exception:
            raise
        else:
            self._stat_meta_info['s'] += 1
            self._last_conn_errors_cnt = 0

        self._parsed_cnt += 1
        return data
