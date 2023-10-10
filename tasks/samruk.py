import csv
import json
from datetime import datetime, timedelta

import luigi
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from settings import SAMRUK_API_HOST, SAMRUK_TOKEN, SAMRUK_API_COMPANY_ID

from tasks.base import ApiToCsv, FtpUploadedOutput, Runner, ExternalCsvLocalInput
from tcomextetl.common.csv import save_csvrows, dict_to_row
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.extract.samruk_requests import SamrukParser, SamrukPlansRestApiParser
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


SamrukParsersFabric.add('regular', SamrukParser)
SamrukParsersFabric.add('plans', SamrukPlansRestApiParser)


def yesterday():
    return datetime.today() - timedelta(days=1)


class SamrukOutput(ApiToCsv):

    endpoint = luigi.Parameter()
    from_to = luigi.TupleParameter(default=())
    token = luigi.Parameter(default=SAMRUK_TOKEN, visibility=ParameterVisibility.HIDDEN)
    entity = luigi.Parameter(default='content', visibility=ParameterVisibility.HIDDEN)
    company_id = luigi.Parameter(default='941240000193')

    limit = luigi.IntParameter(default=100)
    timeout = luigi.IntParameter(default=2)

    @property
    def url(self):
        return f'{SAMRUK_API_HOST}/{self.endpoint}'

    @property
    def params(self):

        m_from = '{}T00:00:00%2B06:00'
        m_to = '{}T23:59:59.00Z'

        params = dict(
            token=self.token,
            identifier=self.company_id,
            page=0,
            size=self.limit
        )

        if self.from_to:
            params['modifiedFrom'] = m_from.format(self.from_to[0])
            params['modifiedTo'] = m_to.format(self.from_to[1])

        return params


    def run(self):

        parser = SamrukParser(
            self.url,
            params=self.params,
            timeout=self.timeout
        )

        for data in parser:
            save_csvrows(self.output_fpath,
                         [dict_to_row(d, self.struct) for d in data],
                         quotechar='"')
            self.set_status_info(*parser.status_percent)
            rewrite_file(self.stat_fpath, json.dumps(parser.stat))

        self.finalize()


@requires(SamrukOutput)
class SamrukFtpOutput(FtpUploadedOutput):
    pass


class SamrukRunner(Runner):

    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    def requires(self):
        params = self.params
        if not self.all_data:

            params['from_to'] = (
                self.start_date.strftime(DEFAULT_FORMAT),
                self.end_date.strftime(DEFAULT_FORMAT)
            )
        return SamrukFtpOutput(**params)


class SamrukSuppliers(SamrukRunner):

    name = luigi.Parameter('samruk_suppliers')


class SamrukBadSuppliers(SamrukRunner):

    name = luigi.Parameter('samruk_bad_suppliers')


class SamrukPurchases(SamrukRunner):

    name = luigi.Parameter('samruk_purchases')


class SamrukContracts(SamrukRunner):

    name = luigi.Parameter('samruk_contracts')


class SamrukParticipationLots(SamrukRunner):

    name = luigi.Parameter('samruk_participation_lots')


class SamrukDicts(SamrukRunner):

    name = luigi.Parameter('samruk_dicts')


class SamrukPlans(SamrukRunner):

    name = luigi.Parameter('samruk_plans')


class SamrukKztPlanItemsOutput(SamrukOutput):

    def requires(self):
        return ExternalCsvLocalInput(name='samruk_plans')

    def _plans_ids(self):
        _ids = []
        with open(self.input().path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.sep)
            for row in csv_reader:
                _ids.append(row[0])

        return _ids

    def run(self):

        p_ids = self._plans_ids()
        parsed_plans_count = 0
        for p_id in p_ids:

            params = self.params
            params['planId'] = p_id
            self.set_progress_percentage(0)
            parser = SamrukParser(self.url, params=params, timeout=self.timeout)

            for data in parser:
                save_csvrows(self.output_fpath,
                             [dict_to_row(d, self.struct) for d in data],
                             quotechar='"')

                s, p = parser.status_percent
                status = f'Total plans: {len(p_ids)}.  Plan ID: {p_id}. Parsed plans: {parsed_plans_count}'
                status = f'{status} \n {s}'

                self.set_status_info(status, p)
                rewrite_file(self.stat_fpath, json.dumps(parser.stat))

            parsed_plans_count += 1

        self.finalize()


@requires(SamrukKztPlanItemsOutput)
class SamrukKztPlanItemsOutput(FtpUploadedOutput):
    pass


class SamrukKztPlansItems(SamrukRunner):

    name = luigi.Parameter(default='samruk_plan_items')

    def requires(self):
        params = self.params
        return SamrukKztPlanItemsOutput(**params)


if __name__ == '__main__':
    luigi.run()


