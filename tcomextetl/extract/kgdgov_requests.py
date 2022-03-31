from xmltodict import parse
from xml.parsers.expat import ExpatError

from tcomextetl.extract.http_requests import HttpRequest
from tcomextetl.common.exceptions import ExternalSourceError


class KgdGovKzSoapApiParser(HttpRequest):

    def __init__(self, url, request_form, bins_handler, **kwargs):
        super(KgdGovKzSoapApiParser, self).__init__(**kwargs)
        self.url = url
        self.request_form = request_form
        self._raw = None
        self._page = None
        self._parsed_count = 0

    def load(self, params):
        request_xml = self.request_form.format(*params.values())
        r = self.request(self.url, data=request_xml)
        return r.text

    def parse(self):

        if not self._raw:
            raise ExternalSourceError('Empty response')
        try:
            d = parse(self._raw)
        except ExpatError:
            raise ExternalSourceError('Not XML formatted')

        if 'err' in d.keys():
            errcode = d.err.errorcode
            raise ExternalSourceError(f'Errorcode {errcode}')

        # we can get one payment as one dict
        _data = d['payment'] if isinstance(d['payment'], list) else [d['payment']]

        data = []
        for d in _data:
            # no BIN in response
            if d['Summa']:
                d['bin'] = self.params['bin']

            # skip payments without Summa
            if d.get('Summa') is not None:
                data.append(d)

        return data

