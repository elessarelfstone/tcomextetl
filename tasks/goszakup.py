import luigi

from luigi.util import requires
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from tcomextetl.extract.goszakup_requests import GoszakupRestApiParser
from tcomextetl.common.csv import dict_to_csvrow, save_csvrows
from settings import GOSZAKUP_API_HOST, GOSZAKUP_TOKEN


class GoszakupOutput(ApiToCsv):

    url = luigi.Parameter()
    from_to = luigi.TupleParameter(default=())
    limit = luigi.Parameter(default=200)
    anchor_field = luigi.Parameter(default='id')
    token = luigi.Parameter(default=GOSZAKUP_TOKEN)

    def run(self):
        headers = dict()
        headers['Authorization'] = self.token

        # if not self.from_to:
        url = f'{GOSZAKUP_API_HOST}{self.url}'
        parser = GoszakupRestApiParser(url, headers=headers, timeout=0)

        for rows in parser:
            data = [dict_to_csvrow(d, self.struct) for d in rows]
            save_csvrows(self.output_path, data)


class GoszakupCompaniesOutput(GoszakupOutput):
    pass


@requires(GoszakupCompaniesOutput)
class GoszakupCompanyFtpOutput(FtpUploadedOutput):
    pass


class GoszakupCompanies(Runner):

    # start_date = luigi.Parameter(default=)
    # end_date = luigi.Parameter()

    name = luigi.Parameter(default='goszakup_companies')

    def requires(self):

        return GoszakupCompanyFtpOutput(name=self.name,
                                        url='/v3/subject/all')


if __name__ == '__main__':
    luigi.run()
