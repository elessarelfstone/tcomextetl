from datetime import datetime, timedelta

import luigi
from luigi.util import requires

from settings import SAMRUK_API_HOST, SAMRUK_USER, SAMRUK_PASSWORD, SAMRUK_API_COMPANY_ID

from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from tcomextetl.common.csv import save_csvrows, dict_to_csvrow
from tcomextetl.common.dates import era
from tcomextetl.extract.samruk_requests import SamrukRestApiParser
from tcomextetl.common.utils import rewrite_file


def yesterday():
    return datetime.today() - timedelta(days=1)


class SamrukOutput(ApiToCsv):

    endpoint = luigi.Parameter()
    user = luigi.Parameter(default=SAMRUK_USER)
    password = luigi.Parameter(default=SAMRUK_PASSWORD)

    entity = luigi.Parameter(default='content')
    after = luigi.DateParameter(default=None)
    is_kzt = luigi.BoolParameter(default=False)
    company_id = luigi.IntParameter(default=0)

    limit = luigi.IntParameter(default=100)
    timeout = luigi.IntParameter(default=2)

    @property
    def url(self):
        return f'{SAMRUK_API_HOST}/{self.endpoint}'

    @property
    def params(self):
        p = dict(page=0, size=self.limit)

        if self.after:
            p['after'] = self.after

        if self.is_kzt:
            p['login'] = self.user

        if self.company_id:
            p['companyIdentifier'] = self.company_id

        return p

    def run(self):

        auth = {'user': self.user, 'password': self.password}
        parser = SamrukRestApiParser(self.url, params=self.params,
                                     auth=auth, timeout=self.timeout)

        for data in parser:
            save_csvrows(self.output_path,
                         [dict_to_csvrow(d, self.struct) for d in data],
                         quoter='"')
            self.set_status_info(*parser.status_percent)
            rewrite_file(self.stat_file_path, str(parser.stat))

        self.finalize()


@requires(SamrukOutput)
class SamrukFtpOutput(FtpUploadedOutput):
    pass


class SamrukRunner(Runner):

    after = luigi.DateParameter(default=Runner.yesterday())

    @property
    def range(self):
        if self.period == 'range':
            return self.after

        return None

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, **params)


class SamrukSuppliers(SamrukRunner):

    name = luigi.Parameter('samruk_suppliers')


class SamrukBadSuppliers(SamrukRunner):

    name = luigi.Parameter('samruk_bad_suppliers')


class SamrukKztPurchases(SamrukRunner):

    name = luigi.Parameter('samruk_kzt_purchases')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, is_kzt=True, **params)


class SamrukKztContracts(SamrukRunner):

    name = luigi.Parameter('samruk_kzt_contracts')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, is_kzt=True,
                               company_id=SAMRUK_API_COMPANY_ID, **params)


class SamrukKztContractSubjects(SamrukRunner):

    name = luigi.Parameter('samruk_kzt_contract_subjects')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, is_kzt=True,
                               company_id=SAMRUK_API_COMPANY_ID, **params)


class SamrukKztPlans(SamrukRunner):

    name = luigi.Parameter('samruk_kzt_plans')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, is_kzt=True,
                               company_id=SAMRUK_API_COMPANY_ID, **params)





if __name__ == '__main__':
    luigi.run()


