import json
import os
from pathlib import Path

import luigi

from luigi.cmdline import luigi_run
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from luigi.util import requires

from tcomextetl.extract.goszakup_requests import (GoszakupRestApiParser,
                                                  GoszakupGraphQLApiParser)
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import yesterday, n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import GOSZAKUP_TOKEN


host = 'https://ows.goszakup.gov.kz'


class GoszakupOutput(ApiToCsv):

    use_rest = luigi.BoolParameter(default=False)
    from_to = luigi.TupleParameter(default=())
    entity = luigi.Parameter(default='')
    endpoint = luigi.Parameter(default='/v3/graphql')
    timeout = luigi.IntParameter(default=0)
    limit = luigi.IntParameter(default=200)
    token = luigi.Parameter(default=GOSZAKUP_TOKEN)

    @property
    def request_params(self):
        params = dict()

        if self.use_rest:
            params['size'] = self.limit
        else:
            params['limit'] = self.limit
            if self.from_to:
                params['from'], params['to'] = self.from_to

        # resume if there were fails
        if self.resume and os.path.exists(self.stat_fpath):
            next_page_params = self.stat['page_params']
            params.update(next_page_params)

        return params

    @property
    def graphql_query_fpath(self):
        return Path(__file__).parent.parent / 'misc' / 'gql' / f'{self.name}.gql'

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token

        url = f'{host}{self.endpoint}'

        # goszakup_dags.gov.kz provides Rest and GraphQl API services
        # Rest API can't retrieve data for specified period
        if self.use_rest:
            parser = GoszakupRestApiParser(
                        url,
                        params=self.request_params,
                        headers=headers,
                        timeout=self.timeout
            )
        else:
            parser = GoszakupGraphQLApiParser(
                        url,
                        self.entity,
                        self.graphql_query_fpath,
                        params=self.request_params,
                        headers=headers,
                        timeout=self.timeout
            )

        # set parsed rows count if resume
        parser.set_parsed_count(self.stat.get('parsed', 0))

        for rows in parser:
            data = [dict_to_row(d, self.struct) for d in rows]
            save_csvrows(self.output_fpath, data)
            self.set_status_info(*parser.status_percent)
            stat = parser.stat
            stat.update(self.request_params)
            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(GoszakupOutput)
class GoszakupFtpOutput(FtpUploadedOutput):
    pass


class GoszakupRunner(Runner):

    name = luigi.Parameter()
    use_rest = luigi.BoolParameter(default=False)
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(GoszakupRunner, self).params
        params['use_rest'] = self.use_rest
        params['resume'] = self.resume

        if not self.use_rest:
            params.pop('endpoint')
            if not self.all_data:
                params['from_to'] = (
                    self.start_date.strftime(DEFAULT_FORMAT),
                    self.end_date.strftime(DEFAULT_FORMAT)
                )
        else:
            params.pop('entity', '')

        return params

    def requires(self):
        return GoszakupFtpOutput(**self.params)


class GoszakupCompanies(GoszakupRunner):

    name = luigi.Parameter('goszakup_companies')
    

class GoszakupContracts(GoszakupRunner):

    name = luigi.Parameter('goszakup_contracts')


class GoszakupUntrusted(GoszakupRunner):
    # don't run for a day
    name = luigi.Parameter('goszakup_untrusted')
    use_rest = luigi.BoolParameter(True)


class GoszakupLots(GoszakupRunner):

    name = luigi.Parameter('goszakup_lots')


class GoszakupTrdBuys(GoszakupRunner):

    name = luigi.Parameter('goszakup_trd_buys')


class GoszakupPlanPoints(GoszakupRunner):

    name = luigi.Parameter('goszakup_plan_points')


class GoszakupPlansKato(GoszakupRunner):

    name = luigi.Parameter('goszakup_plans_kato')


class GoszakupContractUnits(GoszakupRunner):

    name = luigi.Parameter('goszakup_contract_units')


class GoszakupTrdAppOffers(GoszakupRunner):

    name = luigi.Parameter('goszakup_trd_app_offers')


if __name__ == '__main__':
    code = luigi_run()
