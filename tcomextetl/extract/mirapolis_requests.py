from datetime import datetime

from tcomextetl.extract.api_requests import ApiRequests


class MirapolisRequests(ApiRequests):

    def __init__(self, url_template, report_id,  **kwargs):
        super(MirapolisRequests, self).__init__(**kwargs)
        self._url_template = url_template
        self._report_id = report_id
        self._queue = None
        self._total = 0

    @property
    def url(self):
        return self._url_template.format(self._report_id)

    @property
    def total(self):
        return len(self._raw)

    @property
    def page(self):
        return 1

    def load(self, params):
        r = self.request(self.url, params=params)
        return r.json()

    @property
    def size(self):
        return 0

    def parse(self):
        return self._raw

    @property
    def next_page_params(self):
        return {}

    def __iter__(self):

        self._start_date = datetime.now()
        self._raw = self.load(self.params)[1:]

        for d in self.parse():
            self._parsed_count += 1
            self._end_date = datetime.now()
            yield d
