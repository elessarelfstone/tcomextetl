import logging
import requests
import time

from tcomextetl.extract.http_requests import HttpRequest


class QualysDataRequest(HttpRequest):

    def __init__(self, url, headers=None, auth=None, params=None, date_params=None, **kwargs):
        super(QualysDataRequest, self).__init__(**kwargs)
        self.url = url
        self.headers = headers
        self.auth = auth
        self.params = params
        self.date_params = date_params
        self.session = requests.Session()

    def get_raw_data(self):

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.session.post(
                    self.url,
                    headers=self.headers,
                    params=self.params,
                    auth=self.auth,
                    verify=False,
                    timeout=self.timeout
                )

                if response.status_code == 200:
                    return response.text

                logging.error(f"Error: {response.status_code} - {response.text}")
                time.sleep(5)

            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(5)

    def get_qid_info_raw(self):

        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(
                    self.url,
                    headers=self.headers,
                    auth=self.auth,
                    verify=False
                )

                if response.status_code == 200:
                    return response.text
                elif response.status_code == 409:
                    logging.warning(f"Conflict detected (409). Retrying {attempt + 1}/{retries}...")
                    time.sleep(180)
                else:
                    logging.error(f"Error: {response.status_code} - {response.text}")
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}")
                time.sleep(5)

    @property
    def stat(self):
        return {
            'dateFrom': self.date_params['date_from'],
            'dateTo': self.date_params['date_to'],
        }