import json
import io
import os
import zipfile
import gzip
from datetime import datetime
from google.cloud import bigquery
from google.oauth2 import service_account
from math import floor
from pathlib import Path

from tcomextetl.extract.http_requests import HttpRequest

from settings import TEMP_PATH


class AituRequests(HttpRequest):

    def __init__(
            self,
            project_id,
            url,
            params=None,
            headers=None,
            auth=None,
            timeout=None
    ):
        super().__init__(
            params=params,
            headers=headers,
            auth=auth,
            timeout=timeout
        )

        # retrieve zip body
        r = self.request(url)
        zip_file = io.BytesIO(r.content)

        root_path = Path(TEMP_PATH) / 'aitu' / datetime.now().strftime('%Y%m%d%H%M%S')

        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(root_path)

        self._files = []

        project_path = root_path / str(project_id)
        for filename in os.listdir(project_path):
            if filename.endswith('.gz'):
                f_path = Path(project_path) / filename
                self._files.append(f_path)

        self._parsed_count = 0
        self._parsed_files = 0

    @property
    def status_percent(self):
        p = floor((self._parsed_files * 100) / len(self._files))
        s = f'Parsed {self._parsed_count}'
        return s, p

    @property
    def stat(self):
        return {'parsed': self._parsed_count, 'files': self._parsed_files}

    @property
    def load(self):

        data = []
        for f in self._files:
            with gzip.open(f, 'rt') as file:
                for line in file:
                    json_data = json.loads(line)
                    if json_data.get('event_type') not in ['session_start', 'session_end']:
                        data.append(json_data)

        return data

    def __iter__(self):

        for f in self._files:
            data = []
            with gzip.open(f, 'rt') as file:
                for line in file:
                    json_data = json.loads(line)
                    if json_data.get('event_type') not in ['session_start', 'session_end']:
                        data.append(json_data)
                        self._parsed_count += 1  # Increment count by 1 for each valid event
            if data:  # Only yield if there's data to return
                yield data
            self._parsed_files += 1
            os.remove(f)  # Delete the file after reading it


class AituNotificationRequests(HttpRequest):

    def __init__(self, creds_dict, scopes, project, query):
        super(AituNotificationRequests, self).__init__()
        self.creds_dict = creds_dict
        self.scopes = scopes
        self.project = project
        self.query = query

    @property
    def stat(self) -> dict:
        return {}

    def load(self):
        credentials = service_account.Credentials.from_service_account_info(
            self.creds_dict,
            scopes=self.scopes)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        query_job = client.query(self.query)
        return query_job.result()
