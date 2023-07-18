import json
from datetime import datetime, time

import luigi

from luigi.cmdline import luigi_run
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.crmsensor_requests import CrmSensor
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import CRMSENSOR_PASS, CRMSENSOR_USER


host = 'https://host.crmsensor.com/api/external/kaztelChecklists'


class CrmSensorOutput(CsvFileOutput):

    survey_ids = luigi.TupleParameter()
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=CRMSENSOR_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=CRMSENSOR_PASS, visibility=ParameterVisibility.HIDDEN)

    @property
    def request_params(self):
        params = dict()
        params['dateFrom'], params['dateTo'] = self.from_to
        params['surveyIds'] = self.survey_ids
        return params

    def run(self):
        headers = dict()

        headers['X-Auth-User'] = self.user
        headers['X-Auth-Password'] = self.password
        headers['Content-Type'] = 'application/json'

        parser = CrmSensor(
            host,
            params=self.request_params,
            headers=headers
        )

        row_count = 0
        for rows in parser:
            data = [dict_to_row(d, self.struct) for d in rows]
            save_csvrows(self.output_fpath, data)
            row_count += len(rows)

        stat = parser.stat
        stat.update(self.request_params)
        stat.update({'parsed': row_count})
        rewrite_file(self.success_fpath, json.dumps(stat))


@requires(CrmSensorOutput)
class CrmSensorOutputFtpOutput(FtpUploadedOutput):
    pass


class CrmSensorRunner(Runner):

    name = luigi.Parameter()
    use_rest = luigi.BoolParameter(default=False)
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(CrmSensorRunner, self).params
        s_date = datetime.combine(self.start_date, datetime.min.time()).isoformat()
        e_date = datetime.combine(self.end_date, time(23, 59, 59)).isoformat()
        params['from_to'] = (
            s_date,
            e_date
        )

        return params

    def requires(self):
        return CrmSensorOutputFtpOutput(**self.params)


class CrmsensorCheckList(CrmSensorRunner):

    name = luigi.Parameter('crmsensor_checklist')


if __name__ == '__main__':
    code = luigi_run()
