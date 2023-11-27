import json
import io
import os
import zipfile
import gzip
from datetime import datetime, timedelta
from math import floor
from pathlib import Path

import pandas as pd

from tcomextetl.common.exceptions import ExternalSourceError
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

        root_path = Path(TEMP_PATH) / 'aitu_dags'

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

    def load(self):

        data = []
        for f in self._files:
            with gzip.open(f, 'rt') as file:
                for line in file:
                    json_data = json.loads(line)
                    data.append(json_data)

        return data

    def __iter__(self):

        for f in self._files:
            with gzip.open(f, 'rt') as file:
                for line in file:
                    json_data = json.loads(line)
                    data = [json_data]
                    yield data
                    self._parsed_count += len(data)
                    self._parsed_files += 1