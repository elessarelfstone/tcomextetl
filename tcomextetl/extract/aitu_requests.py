import json
import io
import os
import zipfile
import gzip
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.extract.http_requests import HttpRequest

from settings import TEMP_PATH


class AituRequests(HttpRequest):

    def __init__(
        self,
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

        root_path = Path(TEMP_PATH) / 'aitu'

        with zipfile.ZipFile(zip_file, 'r') as z:
            z.extractall(root_path)

        self._files = []
        for filename in os.listdir(root_path):
            if filename.endswith('.gz'):
                f_path = Path(root_path) / filename
                self._files.append(f_path)

    def load(self):

        data = []
        for f in self._files:
            with gzip.open(f, 'rt') as file:
                for line in file:
                    json_data = json.loads(line)
                    data.append(json_data)

        return data





