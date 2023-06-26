import csv
import json
from datetime import datetime, timedelta
from math import floor
from time import sleep

import luigi
import pandas as pd
from luigi.util import requires

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import CSV_QUOTECHAR
from tcomextetl.common.dates import DEFAULT_FORMAT, today, n_days_ago
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import build_fpath, append_file
from tcomextetl.extract.speedtest_requests import SpeedTestDownloader
from settings import TEMP_PATH, SPEEDTEST_USER, SPEEDTEST_PASS

api_url = 'https://intelligence.speedtest.net/extracts'


class SpeedTestOutput(CsvFileOutput):

    from_to = luigi.TupleParameter(default=())
    dataset = luigi.Parameter(default='')
    user = luigi.Parameter(default=SPEEDTEST_USER)
    password = luigi.Parameter(default=SPEEDTEST_PASS)

    @property
    def auth(self):
        return {
            'user': self.user,
            'password': self.password
        }

    def _merge_csvs(self, files) -> tuple[int, int]:
        df = pd.DataFrame()
        row_count = 0
        file_count = 0
        for count, file in enumerate(files):
            data = pd.read_csv(file, sep=',')
            row_count += len(data.index) - 1
            file_count += 1
            df = pd.concat([df, data], axis=0)

            self.set_status_info(
                f'Merging file {file}.',
                floor((count * 100) / len(files))
            )

        df.to_csv(
            self.output_fpath,
            header=False,
            sep=self.sep,
            quoting=csv.QUOTE_ALL,
            quotechar=CSV_QUOTECHAR
        )

        return row_count, file_count

    def run(self):

        wildcard = '*.csv'
        # separator of speedtest csv files
        sep = ','
        d = SpeedTestDownloader(api_url, self.from_to, self.dataset, auth=self.auth)
        datafiles = d.datafiles()
        datafiles.reverse()
        # print(datafiles)
        row_count = 0
        file_count = 0
        # for a one date
        if self.from_to[0] == self.from_to[1]:
            file = list(filter(lambda df: df['date'] == self.from_to[0], datafiles))
            if file:
                af_path = build_fpath(TEMP_PATH, self.name, '.zip')
                d.download(af_path, file.pop()['url'])
                f_path = extract_by_wildcard(af_path, wildcard=wildcard)
                buffer = pd.read_csv(f_path[0], sep=sep)
                buffer.to_csv(
                    self.output_fpath,
                    header=False,
                    sep=self.sep,
                    quoting=csv.QUOTE_ALL,
                    quotechar=CSV_QUOTECHAR
                )
                row_count = len(buffer.index)
                file_count = 1
            else:
                raise ExternalSourceError(f'No data file for date - {self.from_to[0]}')

        else:
            s_date = datetime.strptime(self.from_to[0], DEFAULT_FORMAT)
            e_date = datetime.strptime(self.from_to[1], DEFAULT_FORMAT)
            dates_range = pd.date_range(s_date, e_date, freq='d').strftime('%Y-%m-%d').tolist()

            # check dates
            for dt in dates_range:
                if dt not in [df['date'] for df in datafiles]:
                    raise ExternalSourceError(f'No data file for date - {dt}')

            f_paths = []
            parsed_count = 0
            for dt in dates_range:
                file = list(filter(lambda df: df['date'] == dt, datafiles))
                af_path = build_fpath(TEMP_PATH, self.name, '.zip')
                file = file.pop()
                d.download(af_path, file['url'])
                f_path, *_ = extract_by_wildcard(af_path, wildcard=wildcard)
                f_paths.append(f_path)
                parsed_count += 1
                self.set_status_info(
                    f'File: {file["name"]} .Downloading and unpacking...',
                    floor((parsed_count * 100) / len(dates_range))
                    )
                sleep(5)

            row_count, file_count = self._merge_csvs(f_paths)

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

