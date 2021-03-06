from pathlib import Path

import luigi

from luigi.util import requires
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from tcomextetl.extract.goszakup_requests import (GoszakupRestApiParser,
                                                  GoszakupGraphQLApiParser)
from tcomextetl.common.csv import dict_to_csvrow, save_csvrows
from tcomextetl.common.dates import yesterday
from tcomextetl.common.utils import rewrite_file
from settings import GOSZAKUP_TOKEN


host = 'https://ows.goszakup.gov.kz'


class GoszakupOutput(ApiToCsv):

    entity = luigi.Parameter(default='')
    endpoint = luigi.Parameter(default='/v3/graphql')
    timeout = luigi.Parameter(default=0)
    from_to = luigi.TupleParameter(default=())
    limit = luigi.Parameter(default=200)
    token = luigi.Parameter(default=GOSZAKUP_TOKEN)

    @property
    def params(self):
        params = dict()
        if not self.from_to:
            params['size'] = self.limit
        else:
            params['limit'] = self.limit

            # params['from'], params['to'] = self.from_to[0], self.from_to[1]
            params['from'], params['to'] = self.from_to
        return params

    @property
    def query_fpath(self):
        return Path(__file__).parent.parent / 'misc' / 'gql' / f'{self.name}.gql'

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token

        url = f'{host}{self.endpoint}'

        # goszakup.gov.kz provides Rest and GraphQl API services
        # Rest API doesn't retrieve data for specified period
        if not self.from_to:
            parser = GoszakupRestApiParser(url, params=self.params,
                                           headers=headers, timeout=self.timeout)
        else:

            parser = GoszakupGraphQLApiParser(url, self.entity, self.query_fpath, params=self.params,
                                              headers=headers, timeout=self.timeout)

        for rows in parser:
            data = [dict_to_csvrow(d, self.struct) for d in rows]
            save_csvrows(self.output_path, data)
            self.set_status_info(*parser.status_percent)
            rewrite_file(self.stat_file_path, str(parser.stat))

        self.finalize()


@requires(GoszakupOutput)
class GoszakupFtpOutput(FtpUploadedOutput):
    pass


class GoszakupRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.Parameter(default=yesterday())
    end_date = luigi.Parameter(default=yesterday())

    def requires(self):
        params = self.params
        if self.period == 'all':
            params.pop('entity', None)
            params.pop('anchor_key', None)
        else:
            params.pop('endpoint')
            params['from_to'] = (self.start_date, self.end_date)

        return GoszakupFtpOutput(**params)


class GoszakupCompanies(GoszakupRunner):

    name = luigi.Parameter('goszakup_companies')
    

class GoszakupContracts(GoszakupRunner):

    name = luigi.Parameter('goszakup_contracts')


class GoszakupUntrusted(GoszakupRunner):
    # don't run for a day
    name = luigi.Parameter('goszakup_untrusted')


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


if __name__ == '__main__':
    luigi.run()
