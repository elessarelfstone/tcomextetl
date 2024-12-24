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
    AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY, AMPLITUDE_EGOV_LOGS_API_KEY_2, AMPLITUDE_EGOV_LOGS_SECRET_KEY_2, \
    AMPLITUDE_LOYALTY_PROGRAM_LOGS_API_KEY, AMPLITUDE_LOYALTY_PROGRAM_LOGS_SECRET_KEY

api_url = f"https://amplitude.com/api/2/export"


class AmplitudeOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_API_KEY, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AMPLITUDE_EGOV_LOGS_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)
    amplitude_id = luigi.IntParameter()

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
            self.amplitude_id,
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


@requires(AmplitudeOutput)
class AmplitudeFtpOutput(FtpUploadedOutput):
    pass


class AmplitudeRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AmplitudeRunner, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AmplitudeFtpOutput(**self.params)


class AmplitudeEgovLogs(AmplitudeRunner):
    name = luigi.Parameter('amplitude_egov_logs')


class AmplitudeEgovLogs2(AmplitudeRunner):
    name = luigi.Parameter('amplitude_egov_logs_2')

    def requires(self):
        return AmplitudeFtpOutput(
            user=AMPLITUDE_EGOV_LOGS_API_KEY_2,
            password=AMPLITUDE_EGOV_LOGS_SECRET_KEY_2,
            **self.params
        )


class AmplitudeTelecomkzLogs(AmplitudeRunner):
    name = luigi.Parameter('amplitude_telecomkz_logs')

    def requires(self):
        return AmplitudeFtpOutput(
            user=AMPLITUDE_TELECOMKZ_LOGS_API_KEY,
            password=AMPLITUDE_TELECOMKZ_LOGS_SECRET_KEY,
            **self.params
        )


class AmplitudeLoyaltyProgramLogs(AmplitudeRunner):
    name = luigi.Parameter('amplitude_loyalty_program_logs')

    def requires(self):
        return AmplitudeFtpOutput(
            user=AMPLITUDE_LOYALTY_PROGRAM_LOGS_API_KEY,
            password=AMPLITUDE_LOYALTY_PROGRAM_LOGS_SECRET_KEY,
            **self.params
        )


if __name__ == '__main__':
    luigi.run()
