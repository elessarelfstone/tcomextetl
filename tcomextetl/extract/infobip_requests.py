from tcomextetl.extract.api_requests import ApiRequests
from tcomextetl.extract.http_requests import HttpRequest


class InfobipRestApiParser(ApiRequests):

    def __init__(self, entity, **kwargs):
        super(InfobipRestApiParser, self).__init__(**kwargs)
        self.entity = entity

    def total(self):
        return self._raw[self.entity]

    def page(self):
        pass
