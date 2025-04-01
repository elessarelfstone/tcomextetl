import logging
import requests
import time


class QualysDataRequest:
    def __init__(self, url, headers=None, auth=None, params=None, timeout=300):

        self.url = url
        self.headers = headers or {}
        self.auth = auth
        self.params = params or {}
        self.timeout = timeout
        self.session = requests.Session()

    def get_raw_data(self, params=None):

        request_params = self.params.copy()
        if params:
            request_params.update(params)

        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                response = self.session.post(
                    self.url,
                    headers=self.headers,
                    params=request_params,
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

    def get_qid_info_raw(self, qid_url):

        retries = 3
        for attempt in range(retries):
            try:
                response = self.session.get(
                    qid_url,
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