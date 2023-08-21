import os
import json
import luigi
from datetime import datetime
from io import StringIO
from time import sleep

import attr
import pandas as pd
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tasks.base import ExternalFtpCsvDFInput
from tcomextetl.extract.telecomkz_requests import TelecomkzYandexMetricsRequests

from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT, DEFAULT_DATETIME_FORMAT
from tcomextetl.common.utils import rewrite_file, append_file
from settings import TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN, TELECOMKZ_YANDEX_METRICA_TOKEN

app_metrika_host = 'https://api.appmetrica.yandex.ru'
ya_metrika_host = 'https://api-metrika.yandex.net'
logs_api_url = 'https://api.appmetrica.yandex.ru/logs/v1/export'
reps_api_url = 'https://api.appmetrica.yandex.ru/stat/v1/data.csv'


class TelecomobYandexMetricaLogsOutput(CsvFileOutput):

    app_id = luigi.IntParameter()
    from_to = luigi.TupleParameter()
    entity = luigi.Parameter(default='')
    timeout = luigi.FloatParameter(default=2.0)
    timeout_ban = luigi.FloatParameter(default=30.0)
    token = luigi.Parameter(default=TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN, visibility=ParameterVisibility.HIDDEN)

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
        url = f'{app_metrika_host}/{self.entity}'
        parser = TelecomkzYandexMetricsRequests(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    timeout_ban=self.timeout_ban
        )
        data = parser.load(self.request_params)
        data = data.decode('utf-8').strip()
        data = pd.read_csv(StringIO(data), header=None, sep=",", skiprows=2)
        data.to_csv(self.output_fpath, sep=";", header=False, index=False)
        parsed_count = len(data)
        params = self.request_params
        params.update(dict(parsed=parsed_count))
        rewrite_file(self.success_fpath, json.dumps(params))


@requires(TelecomobYandexMetricaLogsOutput)
class TelecomobYandexMetricaLogsFtpOutput(FtpUploadedOutput):
    pass


class TelecomkzYandexMetricaLogsRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(TelecomkzYandexMetricaLogsRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return TelecomobYandexMetricaLogsFtpOutput(
            token=TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN,
            **self.params
        )


class TelecomobkzYandexMetricaLogsProfiles(TelecomkzYandexMetricaLogsRunner):

    name = luigi.Parameter('telecomobkz_logs_profiles')


class TelecomobkzYandexMetricaLogsEvents(TelecomkzYandexMetricaLogsRunner):

    name = luigi.Parameter('telecomobkz_logs_events')


class TelecomobkzYandexMetricaLogsCrushes(TelecomkzYandexMetricaLogsRunner):

    name = luigi.Parameter('telecomobkz_logs_crashes')


class TelecomYandexMetricaRepsOutput(CsvFileOutput):

    host = luigi.IntParameter()
    id = luigi.IntParameter()
    entity = luigi.Parameter()
    from_to = luigi.TupleParameter()
    metrics = luigi.Parameter(default='', visibility=ParameterVisibility.HIDDEN)
    dimensions = luigi.Parameter(default='', visibility=ParameterVisibility.HIDDEN)
    limit = luigi.Parameter(default=100000, visibility=ParameterVisibility.HIDDEN)
    source = luigi.Parameter(default='', visibility=ParameterVisibility.HIDDEN)
    timeout = luigi.FloatParameter(default=2.0)
    timeout_ban = luigi.FloatParameter(default=30.0)
    token = luigi.Parameter(default=TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN, )

    @property
    def dates_params(self):
        params = dict()
        params['date1'], params['date2'] = self.from_to
        return params

    @property
    def request_params(self):
        params = dict()
        params['id'] = self.id
        params.update(self.dates_params)
        fields = ','.join([a.name for a in attr.fields(self.struct)])
        params['dimensions'] = self.dimensions
        params['metrics'] = self.metrics
        params['limit'] = self.limit
        if self.source:
            params['source'] = self.source
        return params

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token
        url = f'{self.host}/{self.entity}'
        parser = TelecomkzYandexMetricsRequests(
                    url,
                    headers=headers,
                    timeout=self.timeout,
                    timeout_ban=self.timeout_ban
        )
        data = parser.load(self.request_params)
        data = data.decode('utf-8').strip()
        # TODO refactor this with pandas
        data_lines = data.splitlines()[2:]
        parsed_count = len(data_lines)
        data = '\n'.join(data_lines)

        params = self.request_params
        params.update(dict(parsed=parsed_count))

        rewrite_file(self.output_fpath, data)
        rewrite_file(self.success_fpath, json.dumps(params))


@requires(TelecomYandexMetricaRepsOutput)
class TelecomYandexMetricaRepsFtpOutput(FtpUploadedOutput):
    pass


class TelecomobkzYandexMetricaRepsRunner(Runner):

    name = luigi.Parameter()
    timeout = luigi.FloatParameter(default=10.0)
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(TelecomobkzYandexMetricaRepsRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        if self.timeout > params['timeout']:
            params['timeout'] = self.timeout

        return params

    def requires(self):
        return TelecomYandexMetricaRepsFtpOutput(host=app_metrika_host, **self.params)


class TelecomobkzYandexMetricaRepsAcquisitions(TelecomobkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomobkz_reps_acquisitions')


class TelecomobkzYandexMetricaRepsDau(TelecomobkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomobkz_reps_dau')


class TelecomobkzYandexMetricaRepsEvents(TelecomobkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomobkz_reps_events')


class TelecomkzYandexMetricaRepsRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(TelecomkzYandexMetricaRepsRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return TelecomYandexMetricaRepsFtpOutput(
            host=ya_metrika_host,
            token=TELECOMKZ_YANDEX_METRICA_TOKEN,
            **self.params
        )


class TelecomkzYandexMetricaRepsMainVisits(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_main_visits')


class TelecomkzYandexMetricaRepsMainUsers(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_main_users')


class TelecomkzYandexMetricaRepsLK1Visits(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk1_visits')


class TelecomkzYandexMetricaRepsLK1Users(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk1_users')


class TelecomkzYandexMetricaRepsLK2Visits(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk2_visits')


class TelecomkzYandexMetricaRepsLK2Users(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk2_users')


class TelecomkzYandexMetricaRepsLK2Yam2Visits(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk2_yam2_visits')


class TelecomkzYandexMetricaRepsLK2Yam2Users(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_lk2_yam2_users')


class TelecomkzYandexConversionsMetricaRepsOutput(TelecomYandexMetricaRepsOutput):

    conversion_id = None

    ftp_file_mask = luigi.Parameter(visibility=ParameterVisibility.HIDDEN)

    def _conversioned_metrics(self, conversion_id):
        m = self.metrics
        return m.format(conversion_id)

    def requires(self):
        return ExternalFtpCsvDFInput(
            ftp_file_mask=self.ftp_file_mask
        )

    @property
    def request_params(self):
        params = dict()
        params['id'] = self.id
        params.update(self.dates_params)
        fields = ','.join([a.name for a in attr.fields(self.struct)])
        params['dimensions'] = self.dimensions
        params['metrics'] = self._conversioned_metrics(self.conversion_id)
        params['limit'] = self.limit
        if self.source:
            params['source'] = self.source
        return params

    def _conversion_ids_fpath(self) -> str:
        return self._file_path('.ids')

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token
        url = f'{self.host}/{self.entity}'
        parser = TelecomkzYandexMetricsRequests(
            url,
            headers=headers,
            timeout=self.timeout,
            timeout_ban=self.timeout_ban
        )

        if not os.path.exists(self._conversion_ids_fpath()):
            self.input().get(str(self._conversion_ids_fpath()))
        conversions = pd.read_csv(self._conversion_ids_fpath(), sep=';', header=None)
        row_count = 0
        df = pd.DataFrame()
        for _, row in conversions.iterrows():
            conversion_id, conversion_title = row[0], row[1]
            self.conversion_id = conversion_id
            data = parser.load(self.request_params)
            data = data.decode('utf-8').strip()
            data = pd.read_csv(StringIO(data), header=None, sep=",", skiprows=2)
            data.insert(0, 'conversion_title', row[1])
            data.insert(0, 'conversion_id', row[0])
            df = pd.concat([df, data], axis=0)
            row_count += len(data)
            sleep(self.timeout_ban)

        df.to_csv(self.output_fpath, float_format='%.0f', sep=";", header=False, index=False)

        stat = {'parsed': row_count}
        append_file(self.success_fpath, json.dumps(stat))


@requires(TelecomkzYandexConversionsMetricaRepsOutput)
class TelecomYandexConversionsMetricaRepsFtpOutput(FtpUploadedOutput):
    pass


class TelecomkzYandexConversionsMetricaRepsRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(TelecomkzYandexConversionsMetricaRepsRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return TelecomYandexConversionsMetricaRepsFtpOutput(
            host=ya_metrika_host,
            token=TELECOMKZ_YANDEX_METRICA_TOKEN,
            **self.params
        )


class TelecomkzYandexConversionsMetricaRepsMain(TelecomkzYandexConversionsMetricaRepsRunner):
    name = luigi.Parameter('telecomkz_reps_conversions_main')


class TelecomkzYandexConversionsMetricaRepsLK1(TelecomkzYandexConversionsMetricaRepsRunner):
    name = luigi.Parameter('telecomkz_reps_conversions_lk1')


class TelecomkzYandexConversionsMetricaRepsLK2(TelecomkzYandexConversionsMetricaRepsRunner):
    name = luigi.Parameter('telecomkz_reps_conversions_lk2')


if __name__ == '__main__':
    luigi.run()
