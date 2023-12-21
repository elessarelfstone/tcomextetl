import csv
import json
from math import floor
from datetime import datetime, timedelta
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
from settings import AITU_API_KEY, AITU_SECRET_KEY

api_url = f"https://amplitude.com/api/2/export"
amplitude_id = 505199


class AituOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AITU_API_KEY, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AITU_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)

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
            amplitude_id,
            api_url,
            params=params,
            auth=self.auth
        )

        for d in parser:

            save_csvrows(self.output_fpath,
                         [dict_to_row(_d, self.struct, '$') for _d in d],
                         quotechar='"')

            self.set_status_info(*parser.status_percent)

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(AituOutput)
class AituFtpOutput(FtpUploadedOutput):
    pass


class AituRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AituRunner, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AituFtpOutput(**self.params)


class AituLogs(AituRunner):

    name = luigi.Parameter('aitu_logs')


if __name__ == '__main__':
    luigi.run()
