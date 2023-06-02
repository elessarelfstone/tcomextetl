import json
import os
from datetime import datetime
from pathlib import Path

import luigi

import attr
from luigi.cmdline import luigi_run
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.telecomob_requests import TelecomobilYandexMetricsRequests
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import yesterday, n_days_ago, DEFAULT_FORMAT, DEFAULT_DATETIME_FORMAT
from tcomextetl.common.utils import rewrite_file, write_binary
from settings import TELECOMOB_YANDEX_METRICA_TOKEN


api_url = 'https://api.appmetrica.yandex.ru/logs/v1/export'


class TelecomobYandexMetricaOutput(CsvFileOutput):

    app_id = luigi.IntParameter()
    from_to = luigi.TupleParameter()
    entity = luigi.Parameter(default='')
    timeout = luigi.FloatParameter(default=2.0)
    timeout_ban = luigi.FloatParameter(default=30.0)
    token = luigi.Parameter(default=TELECOMOB_YANDEX_METRICA_TOKEN, visibility=ParameterVisibility.HIDDEN)

    @property
    def dates_params(self):
        params = dict()
        dt_since, dt_until = self.from_to
        dt_since = datetime.strptime(dt_since, DEFAULT_FORMAT)
        dt_since = dt_since.replace(hour=0, minute=0, second=0).strftime(DEFAULT_DATETIME_FORMAT)
        dt_until = datetime.strptime(dt_until, DEFAULT_FORMAT)
        dt_until = dt_until.replace(hour=23, minute=59, second=59).strftime(DEFAULT_DATETIME_FORMAT)
        params['date_since'], params['date_until'] = dt_since, dt_until
        return params

    @property
    def request_params(self):
        params = dict()
        params['application_id'] = self.app_id
        params.update(self.dates_params)
        fields = ','.join([a.name for a in attr.fields(self.struct)])
        params['fields'] = fields
        return params

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token
        url = f'{api_url}/{self.entity}'
        parser = TelecomobilYandexMetricsRequests(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    timeout_ban=self.timeout_ban
        )
        data = parser.load(self.request_params)
        data = data.decode('utf-8').strip()
        data_lines = data.splitlines()[1:]
        parsed_count = len(data_lines)
        data = '\n'.join(data_lines)

        # parsed_count = len(data.decode('utf-8').split('\n'))
        params = self.request_params
        params.update(dict(parsed=parsed_count))

        # print(parsed_count)
        # write_binary(self.output_fpath, data)
        rewrite_file(self.output_fpath, data)
        rewrite_file(self.success_fpath, json.dumps(params))


@requires(TelecomobYandexMetricaOutput)
class TelecomobYandexMetricaFtpOutput(FtpUploadedOutput):
    pass


class TelecomobYandexMetricaRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(TelecomobYandexMetricaRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return TelecomobYandexMetricaFtpOutput(**self.params)


class TelecomobYandexMetricaClicks(TelecomobYandexMetricaRunner):

    name = luigi.Parameter('telecomob_clicks')


class TelecomobYandexMetricaPostbacks(TelecomobYandexMetricaRunner):

    name = luigi.Parameter('telecomob_postbacks')


class TelecomobYandexMetricaInstallations(TelecomobYandexMetricaRunner):

    name = luigi.Parameter('telecomob_installations')



if __name__ == '__main__':
    luigi.run()
