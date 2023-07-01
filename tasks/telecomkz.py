import json
import luigi

import attr
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.telecomob_requests import TelecomkzYandexMetricsRequests

from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN, TELECOMKZ_YANDEX_METRICA_TOKEN

app_metrika_host = 'https://api.appmetrica.yandex.ru'
ya_metrika_host = 'https://api-metrika.yandex.net'
logs_api_url = 'https://api.appmetrica.yandex.ru/logs/v1/export'
reps_api_url = 'https://api.appmetrica.yandex.ru/stat/v1/data.csv'


class TelecomYandexMetricaRepsOutput(CsvFileOutput):

    host = luigi.IntParameter()
    id = luigi.IntParameter()
    entity = luigi.Parameter()
    from_to = luigi.TupleParameter()
    metrics = luigi.Parameter(default='')
    dimensions = luigi.Parameter(default='')
    limit = luigi.Parameter(default=100000)
    source = luigi.Parameter(default='')
    timeout = luigi.FloatParameter(default=2.0)
    timeout_ban = luigi.FloatParameter(default=30.0)
    token = luigi.Parameter(default=TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN, visibility=ParameterVisibility.HIDDEN)

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


class TelecomobkzYandexMetricaRepAcquisitions(TelecomobkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomobkz_reps_acquisitions')


class TelecomobkzYandexMetricaRepDau(TelecomobkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomobkz_reps_dau')


class TelecomobkzYandexMetricaRepEvents(TelecomobkzYandexMetricaRepsRunner):

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


class TelecomkzYandexMetricaRepMainVisits(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_main_visits')


class TelecomkzYandexMetricaRepMainUsers(TelecomkzYandexMetricaRepsRunner):

    name = luigi.Parameter('telecomkz_reps_main_users')


if __name__ == '__main__':
    luigi.run()
