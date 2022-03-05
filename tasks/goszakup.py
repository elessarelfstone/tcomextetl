import luigi

from luigi.util import requires
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from tcomextetl.extract.goszakup_requests import GoszakupRestApiParser, GoszakupGraphQLApiParser
from tcomextetl.common.csv import dict_to_csvrow, save_csvrows
from tcomextetl.common.utils import append_file
from settings import GOSZAKUP_REST_API_HOST, GOSZAKUP_TOKEN


class GoszakupOutput(ApiToCsv):

    entity = luigi.Parameter(default='')
    endpoint = luigi.Parameter(default='/v3/graphql')
    timeout = luigi.Parameter(default=0)
    from_to = luigi.TupleParameter(default=())
    limit = luigi.Parameter(default=200)
    anchor_key = luigi.Parameter(default='id')
    token = luigi.Parameter(default=GOSZAKUP_TOKEN)

    @property
    def params(self):
        params = dict()
        params['size'] = self.limit
        return params

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token

        url = f'{GOSZAKUP_REST_API_HOST}{self.endpoint}'
        if not self.from_to:
            parser = GoszakupRestApiParser(url, params=self.params,
                                           headers=headers, timeout=self.timeout)
        else:
            parser = GoszakupGraphQLApiParser(url, self.entity, self.anchor_key,
                                              params=self.params, headers=headers,
                                              timeout=self.timeout)

        for rows in parser:
            data = [dict_to_csvrow(d, self.struct) for d in rows]
            save_csvrows(self.output_path, data)

        append_file(self.success_file_path, 'good')


class GoszakupCompaniesOutput(GoszakupOutput):
    pass


@requires(GoszakupCompaniesOutput)
class GoszakupCompanyFtpOutput(FtpUploadedOutput):
    pass


class GoszakupCompanies(Runner):

    name = luigi.Parameter(default='goszakup_companies')
    start_date = luigi.Parameter(default='2022-02-03')
    end_date = luigi.Parameter(default='2022-02-03')

    def requires(self):
        params = self.params
        if self.period == 'all':
            params.pop('entity', None)
            params.pop('anchor_key', None)
        else:
            params['from_to'] = (self.start_date, self.end_date)

        print(params)
        return GoszakupCompanyFtpOutput(**params)


if __name__ == '__main__':
    luigi.run()
