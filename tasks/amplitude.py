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
from tcomextetl.extract.amplitude_requests import AmplitudeRequests
from settings import AMPLITUDE_EGOV_LOGS_API_KEY, AMPLITUDE_EGOV_LOGS_SECRET_KEY, AMPLITUDE_TELECOMKZ_LOGS_API_KEY, \
    AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY, AMPLITUDE_EGOV_LOGS_API_KEY_2, AMPLITUDE_EGOV_LOGS_SECRET_KEY_2

api_url = f"https://amplitude.com/api/2/export"
amplitude_egov_id = 333828
amplitude_telecomkz_id = 333854
amplitude_egov_id_2 = 622300


class AmplitudeEgovOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_API_KEY, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)

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

        parser = AmplitudeRequests(
            amplitude_egov_id,
            api_url,
            params=params,
            auth=self.auth
        )

        if parser.valid_zip:  # Flag to track ZIP file validity
            for d in parser:
                save_csvrows(self.output_fpath,
                             [dict_to_row(_d, self.struct, '$') for _d in d],
                             quotechar='"')

                self.set_status_info(*parser.status_percent)
        else:
            with open(self.output_fpath, 'w') as f:
                f.write('')  # Write an empty file

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(AmplitudeEgovOutput)
class AmplitudeEgovFtpOutput(FtpUploadedOutput):
    pass


class AmplitudeEgovRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AmplitudeEgovRunner, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AmplitudeEgovFtpOutput(**self.params)


class AmplitudeEgovLogs(AmplitudeEgovRunner):
    name = luigi.Parameter('amplitude_egov_logs')


class AmplitudeEgovOutput2(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_API_KEY_2, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_SECRET_KEY_2, visibility=ParameterVisibility.HIDDEN)

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

        parser = AmplitudeRequests(
            amplitude_egov_id_2,
            api_url,
            params=params,
            auth=self.auth
        )

        if parser.valid_zip:  # Flag to track ZIP file validity
            for d in parser:
                save_csvrows(self.output_fpath,
                             [dict_to_row(_d, self.struct, '$') for _d in d],
                             quotechar='"')

                self.set_status_info(*parser.status_percent)
        else:
            with open(self.output_fpath, 'w') as f:
                f.write('')  # Write an empty file

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(AmplitudeEgovOutput2)
class AmplitudeEgovFtpOutput2(FtpUploadedOutput):
    pass


class AmplitudeEgovRunner2(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AmplitudeEgovRunner2, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AmplitudeEgovFtpOutput2(**self.params)


class AmplitudeEgovLogs2(AmplitudeEgovRunner2):
    name = luigi.Parameter('amplitude_egov_logs_2')


class AmplitudeTelecomkzOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AMPLITUDE_TELECOMKZ_LOGS_API_KEY, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)

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

        parser = AmplitudeRequests(
            amplitude_telecomkz_id,
            api_url,
            params=params,
            auth=self.auth
        )

        if parser.valid_zip:  # Flag to track ZIP file validity
            for d in parser:
                save_csvrows(self.output_fpath,
                             [dict_to_row(_d, self.struct, '$') for _d in d],
                             quotechar='"')

                self.set_status_info(*parser.status_percent)
        else:
            with open(self.output_fpath, 'w') as f:
                f.write('')  # Write an empty file

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(AmplitudeTelecomkzOutput)
class AmplitudeTelecomkzFtpOutput(FtpUploadedOutput):
    pass


class AmplitudeTelecomkzRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AmplitudeTelecomkzRunner, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AmplitudeTelecomkzFtpOutput(**self.params)


class AmplitudeTelecomkzLogs(AmplitudeTelecomkzRunner):
    name = luigi.Parameter('amplitude_telecomkz_logs')


if __name__ == '__main__':
    luigi.run()
