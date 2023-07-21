from datetime import datetime


from tcomextetl.extract.api_requests import ApiRequests


class IotRequestsParser(ApiRequests):

    def __init__(self, url, json,  **kwargs):
        super(IotRequestsParser, self).__init__(**kwargs)
        self.url = url
        self._queue = None
        self._total = 0
        self.json = json

    @property
    def total(self):
        return self._total

    @property
    def page(self):
        return 1

    def load(self, params):
        r = self.request(self.url, params=params, json=self.json)
        # print(r.json())
        print(r.text)
        return r.json()

    @property
    def size(self):
        return self.params['limit']

    def parse(self):
        return self._raw['DATA']

    @property
    def next_page_params(self):
        return {}

    def __iter__(self):

        self._start_date = datetime.now()
        self._raw = self.load(self.params)
        # print(self._raw)

        for d in self.parse():
            self._parsed_count += 1
            self._end_date = datetime.now()
            yield d


# p = IotRequestsParser('https://kt-iot.kz/apps/ktbss/v1/report/',
#                         json={
#                             "TOKEN": "c099ab0f422ebb901d4fcdb20de42af3cccc1471",
#                             "FROM_DATE": "01.07.2023",
#                             "TO_DATE": "02.07.2023"
#                            },
#     )
#
# for j in p:
#     print(j)