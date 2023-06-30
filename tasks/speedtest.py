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
from tcomextetl.common.csv import CSV_QUOTECHAR
from tcomextetl.common.dates import DEFAULT_FORMAT, n_days_ago
from tcomextetl.common.utils import build_fpath, append_file
from tcomextetl.extract.speedtest_requests import SpeedTestDownloader
from settings import TEMP_PATH, SPEEDTEST_USER, SPEEDTEST_PASS

api_url = 'https://intelligence.speedtest.net/extracts'


class SpeedTestOutput(CsvFileOutput):

    from_to = luigi.TupleParameter(default=())
    dataset = luigi.Parameter(default='')
    user = luigi.Parameter(default=SPEEDTEST_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=SPEEDTEST_PASS, visibility=ParameterVisibility.HIDDEN)

    @property
    def auth(self):
        return {
            'user': self.user,
            'password': self.password
        }

    def run(self):

        wildcard = '*.csv'
        # separator of speedtest csv files
        d = SpeedTestDownloader(
            api_url,
            *self.from_to,
            self.dataset,
            auth=self.auth
        )
        f_paths = []
        d_count = 0

        # download and unpack
        for file in d:
            af_path = build_fpath(TEMP_PATH, self.name, '.zip')
            d.download(af_path, file['url'])
            # there is always only one csv file in zip archive
            f_path, *_ = extract_by_wildcard(af_path, wildcard=wildcard)
            f_paths.append(f_path)
            d_count += 1
            self.set_status_info(
                f'File: {file["name"]} .Downloading and unpacking...',
                floor((d_count * 100) / d.length)
            )
            sleep(5)

        df = pd.DataFrame()
        row_count = 0
        file_count = 0

        # merging csv files
        for count, file in enumerate(f_paths, start=1):
            data = pd.read_csv(file, sep=',')
            row_count += len(data.index) - 1
            # file_count += 1
            df = pd.concat([df, data], axis=0)
            file_count = count
            self.set_status_info(
                f'Merging file {file}.',
                floor((count * 100) / len(f_paths))
            )
        # there is always extra column - id, so rid off it
        df.drop(columns=df.columns[0], axis=1, inplace=True)

        df.to_csv(
            self.output_fpath,
            header=False,
            sep=self.sep,
            quoting=csv.QUOTE_ALL,
            quotechar=CSV_QUOTECHAR
        )

        stat = {'file_count': file_count, 'row_count': row_count}
        append_file(self.success_fpath, json.dumps(stat))


@requires(SpeedTestOutput)
class GoszakupFtpOutput(FtpUploadedOutput):
    pass


class SpeedTestRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(SpeedTestRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return GoszakupFtpOutput(**self.params)


class SpeedtestSensitiveData(SpeedTestRunner):

    name = luigi.Parameter('speedtest_sensitive_data')


class SpeedtestFixedNetworkPerformance(SpeedTestRunner):

    name = luigi.Parameter('speedtest_fixed_network_performance')


if __name__ == '__main__':
    luigi.run()
