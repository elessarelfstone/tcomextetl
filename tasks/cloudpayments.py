from settings import CLOUDPAYMENTS_USER, CLOUDPAYMENTS_PASS
import luigi
from luigi.parameter import ParameterVisibility
from luigi.util import requires
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner

from tcomextetl.common.csv import save_csvrows, dict_to_row
from tcomextetl.common.utils import rewrite_file
import json

from tcomextetl.extract.cloudpayments_requests import CloudPaymentsParser

cloudpayments_url = 'https://api.cloudpayments.kz'


class CloudPaymentsListOutput(ApiToCsv):
    endpoint = luigi.Parameter()

    user = luigi.Parameter(default=CLOUDPAYMENTS_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=CLOUDPAYMENTS_PASS, visibility=ParameterVisibility.HIDDEN)

    from_to = luigi.TupleParameter(default=())
    timeout = luigi.IntParameter(default=4)
    timeout_ban = luigi.IntParameter(default=2)

    @property
    def url(self):
        return f'{cloudpayments_url}{self.endpoint}'

    @property
    def request_params(self):
        return {}

    def run(self):
        auth = {'user': self.user, 'password': self.password}
        dates = self.from_to
        parser = CloudPaymentsParser(self.url, dates, params=self.request_params,
                                     auth=auth, timeout=self.timeout, timeout_ban=self.timeout_ban)

        # set parsed rows count if resume
        parser.set_parsed_count(self.stat.get('parsed', 0))

        for data in parser:
            save_csvrows(self.output_fpath,
                         [dict_to_row(d, self.struct) for d in data], quotechar='"')
            self.set_status_info(*parser.status_percent)
            stat = parser.stat
            stat.update(self.request_params)
            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(CloudPaymentsListOutput)
class CloudPaymentsListFtpOutput(FtpUploadedOutput):
    pass


class CloudPaymentsRunner(Runner):
    start_date = luigi.Parameter(default=Runner.yesterday())
    end_date = luigi.Parameter(default=Runner.yesterday())

    def requires(self):
        params = self.params

        if not self.all_data:
            params['from_to'] = (self.start_date, self.end_date)

        return CloudPaymentsListFtpOutput(**params)


class CloudPaymentsList(CloudPaymentsRunner):
    name = luigi.Parameter('cloud_payments_list')


if __name__ == '__main__':
    luigi.run()
