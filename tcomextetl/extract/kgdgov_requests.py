from json import dumps, loads
from xmltodict import parse
from xml.parsers.expat import ExpatError

from tcomextetl.extract.http_requests import HttpRequest
from tcomextetl.common.exceptions import ExternalSourceError


class KgdGovKzSoapApiError(Exception):
    pass


class KgdGovKzSoapApiResponseError(Exception):
    pass


class KgdGovKzSoapApiParser(HttpRequest):

    def __init__(self, url, request_form, **kwargs):
        super(KgdGovKzSoapApiParser, self).__init__(**kwargs)
        self.url = url
        self.request_form = request_form
        self._raw = None
        self._page = None
        self._parsed_count = 0

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, val):
        self._raw = val

    def load(self, params):
        request_xml = self.request_form.format(*params.values())
        r = self.request(self.url, data=request_xml)
        return r.text

    def parse(self):

        if not self._raw:
            raise KgdGovKzSoapApiResponseError('Empty response')
        try:
            raw_json = loads(dumps(parse(self._raw)))
            answer = raw_json['answer']
        except ExpatError:
            raise KgdGovKzSoapApiResponseError('Not XML formatted')

        if 'err' in answer.keys():
            errcode = answer.err.errorcode
            raise KgdGovKzSoapApiError(f'Errorcode {errcode}')

        # we can get one payment as single dict
        payments = answer['payment'] if isinstance(answer['payment'], list) else [answer['payment']]

        data = []
        for d in payments:
            # no BIN in response
            if d['Summa']:
                d['bin'] = answer['IIN_BIN']

            # skip payments without Summa
            if d.get('Summa') is not None:
                data.append(d)

        return data



