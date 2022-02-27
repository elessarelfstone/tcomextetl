import luigi
from time import sleep

from luigi.util import requires

from tasks.base import Base, FtpUploadedOutput, Runner
from tasks.xls import WebExcelFileParsingToCsv, ArchivedWebExcelFileParsingToCsv
from tcomextetl.extract.sgov_requests import SgovApiRCutParser
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import build_fpath, append_file, read_file
from settings import TEMP_PATH

rcut_legal_entities = 'legal_entities'
rcut_legal_branches = 'legal_branches'
rcut_joint_ventures = 'joint_ventures'
rcut_foreign_branches = 'foreign_branches'
rcut_entrepreneurs = 'entrepreneurs'


class SgovKatoOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovKatoOutput)
class SgovKatoFtpOutput(FtpUploadedOutput):
    pass


class SgovKato(Runner):

    name = luigi.Parameter(default='sgov_kato')

    def requires(self):
        return SgovKatoFtpOutput(**self.params)


class SgovOkedOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovOkedOutput)
class SgovOkedFtpOutput(FtpUploadedOutput):
    pass


class SgovOked(Runner):

    name = luigi.Parameter(default='sgov_oked')

    def requires(self):
        return SgovOkedFtpOutput(**self.params)


class SgovMkeisOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovMkeisOutput)
class SgovMkeisFtpOutput(FtpUploadedOutput):
    pass


class SgovMkeis(Runner):

    name = luigi.Parameter(default='sgov_mkeis')

    def requires(self):
        return SgovMkeisFtpOutput(**self.params)


class SgovKurkOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovKurkOutput)
class SgovKurkFtpOutput(FtpUploadedOutput):
    pass


class SgovKurk(Runner):

    name = luigi.Parameter(default='sgov_kurk')

    def requires(self):
        return SgovKurkFtpOutput(**self.params)


class SgovKpvedOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovKpvedOutput)
class SgovKpvedFtpOutput(FtpUploadedOutput):
    pass


class SgovKpved(Runner):

    name = luigi.Parameter(default='sgov_kpved')

    def requires(self):
        return SgovKpvedFtpOutput(**self.params)


class SgovRcutCompaniesLinkOutput(Base):

    name = luigi.Parameter()
    juridical_type_id = luigi.IntParameter()
    prev_period_index = luigi.IntParameter(default=0)
    timeout = luigi.IntParameter(default=200)

    @staticmethod
    def build_fpath(name):
        return build_fpath(TEMP_PATH, name, '.url')

    def output(self):
        return luigi.LocalTarget(SgovRcutCompaniesLinkOutput.build_fpath(self.name))

    def run(self):
        p = SgovApiRCutParser(self.juridical_type_id, self.prev_period_index)

        order_id = p.place_order()

        status_info = f'OrderID : {order_id}. Waiting for url...'
        self.set_status_info(status_info, 50)

        url = None

        while url is None:
            sleep(self.timeout)
            url = p.check_state(order_id)

        append_file(self.output().path, url)
        status_info += '\n' + f' Url: {url}'
        self.set_status_info(status_info, 100)


class SgovRcutCompaniesLinkRunner(Runner):

    def requires(self):
        params = self.params
        del params['date']
        return SgovRcutCompaniesLinkOutput(**params)


class SgovRcutsPrepared(luigi.WrapperTask):

    def requires(self):
        yield SgovRcutCompaniesLinkRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutCompaniesLinkRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutCompaniesLinkRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutCompaniesLinkRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutCompaniesLinkRunner(name=f'sgov_{rcut_entrepreneurs}')


class SgovRcutCompaniesOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovRcutCompaniesOutput)
class SgovRcutCompaniesFtpOutput(FtpUploadedOutput):
    pass


class SgovRcutCompaniesRunner(Runner):

    def requires(self):

        link_task_class = SgovRcutCompaniesLinkOutput

        params = self.params
        del params['juridical_type_id']
        del params['timeout']
        # get prepared url
        params['url'] = read_file(link_task_class.build_fpath(self.name))
        params['wildcard'] = '*.xlsx'

        return SgovRcutCompaniesFtpOutput(**params)


class SgovRcutsCompanies(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutCompaniesRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutCompaniesRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutCompaniesRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutCompaniesRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutCompaniesRunner(name=f'sgov_{rcut_entrepreneurs}')


if __name__ == '__main__':
    luigi.run()
