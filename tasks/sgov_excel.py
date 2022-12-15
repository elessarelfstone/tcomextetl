import luigi
from time import sleep

from luigi.util import requires

from tasks.base import Base, FtpUploadedOutput, Runner
from tasks.xls import WebExcelFileParsingToCsv, ArchivedWebExcelFileParsingToCsv
from tcomextetl.extract.sgov_requests import SgovApiRCutParser
from tcomextetl.common.dates import first_day_of_month
from tcomextetl.common.utils import build_fpath, append_file, read_file
from settings import TEMP_PATH

rcut_legal_entities = 'legal_entities'
rcut_legal_branches = 'legal_branches'
rcut_joint_ventures = 'joint_ventures'
rcut_foreign_branches = 'foreign_branches'
rcut_entrepreneurs = 'entrepreneurs'


class SgovExcelRunner(Runner):

    date = luigi.DateParameter(default=first_day_of_month())


class SgovKatoOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovKatoOutput)
class SgovKatoFtpOutput(FtpUploadedOutput):
    pass


class SgovKato(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kato')

    def requires(self):
        return SgovKatoFtpOutput(**self.params)


class SgovOkedOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovOkedOutput)
class SgovOkedFtpOutput(FtpUploadedOutput):
    pass


class SgovOked(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_oked')

    def requires(self):
        return SgovOkedFtpOutput(**self.params)


class SgovMkeisOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovMkeisOutput)
class SgovMkeisFtpOutput(FtpUploadedOutput):
    pass


class SgovMkeis(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_mkeis')

    def requires(self):
        return SgovMkeisFtpOutput(**self.params)


class SgovKurkOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovKurkOutput)
class SgovKurkFtpOutput(FtpUploadedOutput):
    pass


class SgovKurk(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kurk')

    def requires(self):
        return SgovKurkFtpOutput(**self.params)


class SgovKpvedOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovKpvedOutput)
class SgovKpvedFtpOutput(FtpUploadedOutput):
    pass


class SgovKpved(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kpved')

    def requires(self):
        return SgovKpvedFtpOutput(**self.params)


class SgovRcutJuridicalLinkOutput(Base):

    name = luigi.Parameter()
    juridical_type_id = luigi.IntParameter()
    prev_period_index = luigi.IntParameter(default=0)
    timeout = luigi.IntParameter(default=200)

    @staticmethod
    def build_fpath(name):
        return build_fpath(TEMP_PATH, name, '.url')

    def output(self):
        return luigi.LocalTarget(SgovRcutJuridicalLinkOutput.build_fpath(self.name))

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


class SgovRcutJuridicalLinkRunner(Runner):

    def requires(self):
        params = self.params
        params.pop('date')
        params.pop('skiptop')
        return SgovRcutJuridicalLinkOutput(**params)


class SgovRcutsPrepared(luigi.WrapperTask):

    def requires(self):
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_entrepreneurs}')


class SgovRcutJuridicalOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovRcutJuridicalOutput)
class SgovRcutJuridicalFtpOutput(FtpUploadedOutput):
    pass


class SgovRcutJuridicalRunner(Runner):

    def requires(self):

        link_task_class = SgovRcutJuridicalLinkOutput

        params = self.params
        del params['juridical_type_id']
        del params['timeout']
        # get prepared url
        params['url'] = read_file(link_task_class.build_fpath(self.name))
        params['wildcard'] = '*.xlsx'

        return SgovRcutJuridicalFtpOutput(**params)


class SgovRcutsJuridical(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_entrepreneurs}')


if __name__ == '__main__':
    luigi.run()
