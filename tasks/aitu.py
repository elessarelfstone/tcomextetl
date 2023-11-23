import csv
import json
from math import floor
from time import sleep

import luigi
import pandas as pd
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import save_csvrows, dict_to_row, CSV_QUOTECHAR
from tcomextetl.common.dates import DEFAULT_FORMAT, n_days_ago
from tcomextetl.common.utils import build_fpath, append_file, rewrite_file
from tcomextetl.extract.aitu_requests import AituRequests
from settings import TEMP_PATH, SPEEDTEST_USER, SPEEDTEST_PASS

api_url = f"https://amplitude.com/api/2/export"


class AituOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=SPEEDTEST_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=SPEEDTEST_PASS, visibility=ParameterVisibility.HIDDEN)

    @property
    def auth(self):
        return {
            'user': self.user,
            'password': self.password
        }

    def run(self):

        params = {
            "start": self.from_to[0],
            "end": self.from_to[1]
        }

        parser = AituRequests(
            api_url,
            params=params,
            auth=self.auth
        )

        data = parser.load()
        for d in data:
            save_csvrows(self.output_fpath,
                         [dict_to_row(d, self.struct) for d in data],
                         quotechar='"')
            self.set_status_info(*parser.status_percent)
            rewrite_file(self.stat_fpath, json.dumps(parser.stat))

        self.finalize()
