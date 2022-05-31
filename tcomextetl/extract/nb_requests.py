from datetime import datetime

from bs4 import BeautifulSoup as bs

from tcomextetl.common.dates import DEFAULT_FORMAT
from tcomextetl.extract.http_requests import HttpRequest

rates_url = 'https://nationalbank.kz/ru/exchangerates/ezhednevnye-oficialnye-rynochnye-kursy-valyut'


class NbRatesParser(HttpRequest):
    def __init__(self, **kwargs):
        super(NbRatesParser, self).__init__(**kwargs)
        self._raw = None

    def parse(self):
        soup = bs(self._raw, 'lxml')
        table = soup.find()
        trs = table.find_all('tr')
        data = []
        for tr in trs:
            tds = tr.find_all('td')
            rate = tds[-2].text
            code = tds[-3].text.split('/')[0].strip()
            date = datetime.strftime(datetime.today(), DEFAULT_FORMAT)
            data.append((code, rate, date))

        return data

    def get_rates(self):
        r = self.request(rates_url)
        self._raw = r.text
        return self.parse()
