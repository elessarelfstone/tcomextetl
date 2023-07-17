from tcomextetl.extract.crmsensor_requests import CrmSensor

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

        for rows in parser:
            data = [dict_to_row(d, self.struct) for d in rows]
            save_csvrows(self.output_fpath, data)


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
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return CrmSensorOutputFtpOutput(**self.params)


class CrmsensorCheckList(CrmSensorRunner):

    name = luigi.Parameter('crmsensor_checklist')


if __name__ == '__main__':
    code = luigi_run()