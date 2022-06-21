import json

from tcomextetl.extract.http_requests import HttpRequest
from tcomextetl.common.exceptions import ExternalSourceError

sgov_host = 'stat.gov.kz'

headers = {
    'authority': 'stat.gov.kz',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://stat.gov.kz',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://stat.gov.kz/jur-search/filter',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
}


class SgovApiException(Exception):
    pass


class SgovApiRCutParser(HttpRequest):

    def __init__(self, juridical_type_id, which_last=0):
        super().__init__(headers=headers)
        self.juridical_type_id = juridical_type_id
        self.which_last = which_last

    @property
    def rcuts_list(self):
        r = self.request(f'https://{sgov_host}/api/rcut/en')
        return [rcut['id'] for rcut in r.json()]

    def place_order(self):

        # data for placing order
        juridical_type_info = {"classVersionId": 2153, "itemIds": [self.juridical_type_id]}
        status_info = {"classVersionId": 1989, "itemIds": [1989]}
        data = json.dumps({'conditions': [juridical_type_info, status_info],
                           'stringForMD5': 'string',
                           'cutId': self.rcuts_list[self.which_last]})

        r = self.request(f'https://{sgov_host}/api/sbr/request', data=data)

        payload = r.json()
        order_id = payload.get('obj')
        self._stat_meta_info['order_id'] = order_id

        if order_id is None:
            raise ExternalSourceError('Could not parse response.')

        return order_id

    def check_head(self, url: str) -> bool:
        r = self.head(url)
        return True if r.status_code == 200 else False

    def check_state(self, order_id):

        """ Check status of placed order for rcut.
            If it's ready returns url.
        """

        r = self.request(f'https://{sgov_host}/api/sbr/requestResult/{order_id}/ru')
        payload = r.json()

        success = payload.get('success')
        obj = payload.get('obj')
        state = payload.get('description')

        if success is None:
            raise ExternalSourceError('Could not parse response.')

        # there are so many conditions
        # cause stat.gov.kz API do not work properly
        if success is True:
            if obj:
                guid = obj.get('fileGuid')
                url = f'https://{sgov_host}/api/sbr/download?bucket=SBR_UREQUEST&guid={guid}'
                if self.check_head(url):
                    self._stat_meta_info['guid'] = guid
                    return url
                else:
                    return None
            else:
                return None
        else:
            raise SgovApiException('Rcut file guid not available.')
