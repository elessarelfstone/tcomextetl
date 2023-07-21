import json
from datetime import timedelta

import luigi

from luigi.cmdline import luigi_run
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.iot_requests import IotRequestsParser
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import IOT_TOKEN


host = 'https://kt-iot.kz/apps/ktbss/v1/report/'


class IotOutput(CsvFileOutput):

    from_to = luigi.TupleParameter(default=())
    token = luigi.Parameter(default=IOT_TOKEN, visibility=ParameterVisibility.HIDDEN)


    @property
    def request_params(self):
        return None

    def run(self):
        json_body = dict()

        json_body['FROM_DATE'], json_body['TO_DATE'] = self.from_to

        parser = IotRequestsParser(
            host,
            json={**json_body, "TOKEN": self.token}
        )

        row_count = 0
        buffer = []
        for d in parser:
            buffer.append(d)
            save_csvrows(self.output_fpath, [dict_to_row(d, self.struct) for d in buffer])
            buffer.clear()
            row_count += 1

        stat = parser.stat
        stat.update(json_body)
        stat.update({'parsed': row_count})
        rewrite_file(self.success_fpath, json.dumps(stat))


@requires(IotOutput)
class IotOutputFtpOutput(FtpUploadedOutput):
    pass


class IotRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(IotRunner, self).params
        e_date = self.end_date + timedelta(days=1)

        params['from_to'] = (
            self.start_date.strftime('%d.%m.%Y'),
            e_date.strftime('%d.%m.%Y')
        )
        return params

    def requires(self):
        return IotOutputFtpOutput(**self.params)


class IotStat(IotRunner):

    name = luigi.Parameter('iot_stat')


if __name__ == '__main__':
    code = luigi.run()
