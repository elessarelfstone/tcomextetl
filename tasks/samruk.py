import csv
import json
from datetime import datetime, timedelta
from math import floor

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


class SamrukDetailOutput(SamrukOutput):

    master_dataset_name = luigi.Parameter()
    foreign_key_param = luigi.Parameter()

    def requires(self):
        return ExternalCsvLocalInput(name=self.master_dataset_name)

    def _plans_ids(self):
        _ids = []
        with open(self.input().path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.sep)
            for row in csv_reader:
                _ids.append(row[0])

        return _ids

    def run(self):

        p_ids = self._plans_ids()
        parsed_count = 0
        for i, p_id in enumerate(p_ids):

            params = self.params
            params[self.foreign_key_param] = p_id
            parser = SamrukParser(self.url, params=params, timeout=self.timeout)

            for data in parser:
                save_csvrows(self.output_fpath,
                             [dict_to_row(d, self.struct) for d in data],
                             quotechar='"')

                status = f'Total: {len(p_ids)}. Parsed: {parsed_count}'
                p = floor((i * 100) / len(p_ids))

                self.set_status_info(status, p)
                rewrite_file(self.stat_fpath, json.dumps(parser.stat))

            parsed_count += 1

        self.finalize()


@requires(SamrukDetailOutput)
class SamrukFtpDetailOutput(FtpUploadedOutput):
    pass


class SamrukPlanItems(SamrukRunner):

    name = luigi.Parameter(default='samruk_plan_items')
    all_data = luigi.BoolParameter(default=True)

    def requires(self):
        params = self.params
        return SamrukFtpDetailOutput(master_dataset_name='samruk_plans',
                                     foreign_key_param='planId',
                                     **params)


class SamrukContractItems(SamrukRunner):

    name = luigi.Parameter(default='samruk_contract_items')
    all_data = luigi.BoolParameter(default=True)

    def requires(self):
        params = self.params
        return SamrukFtpDetailOutput(master_dataset_name='samruk_contracts',
                                     foreign_key_param='contractCardId',
                                     **params)


class SamrukContractItemDeliveries(SamrukRunner):

    name = luigi.Parameter(default='samruk_contract_item_deliveries')
    all_data = luigi.BoolParameter(default=True)

    def requires(self):
        params = self.params
        return SamrukFtpDetailOutput(master_dataset_name='samruk_contract_items',
                                     foreign_key_param='contractItemId',
                                     **params)


class SamrukEntries(SamrukRunner):

    name = luigi.Parameter(default='samruk_entries')
    all_data = luigi.BoolParameter(default=True)

    def requires(self):
        params = self.params
        return SamrukFtpDetailOutput(master_dataset_name='samruk_dicts',
                                     foreign_key_param='dictionaryId',
                                     **params)


if __name__ == '__main__':
    luigi.run()