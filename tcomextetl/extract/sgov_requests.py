import json

from tcomextetl.extract.http_requests import HttpRequest

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

        return r.json()['obj']

    def check_state(self, order_id):

        """ Check readiness of placed order for rcut.
            If it's ready returns url.
        """

        r = self.request(f'https://{sgov_host}/api/sbr/requestResult/{order_id}/en')
        r_data = r.json()
        if r_data.get('success') is True:
            if r_data.get('description') == 'Обработан':
                f_guid = r_data.get('obj', {}).get('fileGuid')
                return f'https://{sgov_host}/api/sbr/download?bucket=SBR&guid={f_guid}'
            elif r_data.get('description') == 'В обработке':
                return None
        else:
            raise SgovApiException('Rcut file guid not available.')