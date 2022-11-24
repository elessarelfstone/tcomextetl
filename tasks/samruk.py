import csv
from datetime import datetime, timedelta

import luigi
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from settings import SAMRUK_API_HOST, SAMRUK_USER, SAMRUK_PASSWORD, SAMRUK_API_COMPANY_ID

from tasks.base import ApiToCsv, FtpUploadedOutput, Runner, ExternalCsvLocalInput
from tcomextetl.common.csv import save_csvrows, dict_to_csvrow
from tcomextetl.extract.samruk_requests import SamrukRestApiParser, SamrukPlansRestApiParser
from tcomextetl.common.utils import rewrite_file


class SamrukParsersFabric:

    _parsers = {}

    @classmethod
    def add(cls, name, parser):
        cls._parsers[name] = parser

    @classmethod
    def get(cls, name):
        try:
            return cls._parsers[name]
        except KeyError:
            raise ValueError(name)


SamrukParsersFabric.add('regular', SamrukRestApiParser)
SamrukParsersFabric.add('plans', SamrukPlansRestApiParser)


def yesterday():
    return datetime.today() - timedelta(days=1)


class SamrukOutput(ApiToCsv):

    endpoint = luigi.Parameter()
    user = luigi.Parameter(default=SAMRUK_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=SAMRUK_PASSWORD, visibility=ParameterVisibility.HIDDEN)

    entity = luigi.Parameter(default='content', visibility=ParameterVisibility.HIDDEN)
    after = luigi.DateParameter(default=None)
    is_kzt = luigi.BoolParameter(default=False, visibility=ParameterVisibility.HIDDEN)
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

        if 'plan' in self.url:
            parser = SamrukPlansRestApiParser(self.url, params=self.params,
                                              auth=auth, timeout=self.timeout)

        for data in parser:
            save_csvrows(self.output_path,
                         [dict_to_csvrow(d, self.struct) for d in data],
                         quotechar='"')
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


class SamrukCerts(SamrukRunner):

    name = luigi.Parameter('samruk_certs')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, **params)


class SamrukDicts(SamrukRunner):

    name = luigi.Parameter('samruk_dicts')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, **params)


class SamrukKztPlans(SamrukRunner):

    name = luigi.Parameter('samruk_kzt_plans')

    def requires(self):
        params = self.params
        return SamrukFtpOutput(after=self.range, is_kzt=True,
                               company_id=SAMRUK_API_COMPANY_ID, **params)


class SamrukKztPlanItemsOutput(SamrukOutput):

    def requires(self):
        return ExternalCsvLocalInput(name='samruk_kzt_plans')

    def _plans_ids(self):
        _ids = []
        with open(self.input().path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.sep)
            for row in csv_reader:
                _ids.append(row[0])

        return _ids

    def run(self):

        auth = {'user': self.user, 'password': self.password}

        p_ids = self._plans_ids()
        parsed_plans_count = 0
        for p_id in p_ids:

            params = self.params
            params['planId'] = p_id
            self.set_progress_percentage(0)
            parser = SamrukPlansRestApiParser(self.url, params=params,
                                              auth=auth, timeout=self.timeout)

            for data in parser:
                _data = []
                for d in data:
                    _data.append({**d, **{'planId': p_id}})

                save_csvrows(self.output_path,
                             [dict_to_csvrow(d, self.struct) for d in _data],
                             quotechar='"')

                s, p = parser.status_percent
                status = f'Total plans: {len(p_ids)}.  Plan ID: {p_id}. Parsed plans: {parsed_plans_count}'
                status = f'{status} \n {s}'

                self.set_status_info(status, p)
                rewrite_file(self.stat_file_path, str(parser.stat))

            parsed_plans_count += 1

        self.finalize()


@requires(SamrukKztPlanItemsOutput)
class SamrukKztPlanItemsOutput(FtpUploadedOutput):
    pass


class SamrukKztPlansItems(SamrukRunner):

    name = luigi.Parameter(default='samruk_kzt_plan_items')

    def requires(self):
        params = self.params
        return SamrukKztPlanItemsOutput(after=self.range, **params)


if __name__ == '__main__':
    luigi.run()


