import luigi
from time import sleep

from luigi.util import requires

from tasks.base import FtpUploadedOutput, Runner
from tasks.xls import WebExcelFileParsingToCsv, ArchivedWebExcelFileParsingToCsv
from tcomextetl.common.utils import build_fpath, append_file
from tcomextetl.extract.sgov_requests import SgovApiRCutParser
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


class SgovRcutCompaniesLink(luigi.Task):

    name = luigi.Parameter()
    juridical_type_id = luigi.IntParameter()
    which_last = luigi.IntParameter(default=0)
    timeout = luigi.IntParameter(default=200)

    def output(self):
        return luigi.LocalTarget(build_fpath(TEMP_PATH, self.name, '.url'))

    def run(self):
        p = SgovApiRCutParser(self.juridical_type_id, self.which_last)

        order_id = p.place_order()
        url = None

        while url is None:
            sleep(self.timeout)
            url = p.check_state(order_id)

        append_file(self.output().path, url)


class SgovRcutsPrepared(luigi.WrapperTask):

    def requires(self):
        yield SgovRcutCompaniesLink(name=f'statgovkz_{rcut_legal_entities}',
                                    juridical_type_id=742679)
        yield SgovRcutCompaniesLink(name=f'statgovkz_{rcut_joint_ventures}',
                                    juridical_type_id=742687)
        yield SgovRcutCompaniesLink(name=f'statgovkz_{rcut_legal_branches}',
                                    juridical_type_id=742680)
        yield SgovRcutCompaniesLink(name=f'statgovkz_{rcut_foreign_branches}',
                                    juridical_type_id=742684)
        yield SgovRcutCompaniesLink(name=f'statgovkz_{rcut_entrepreneurs}',
                                    juridical_type_id=742681)


if __name__ == '__main__':
    luigi.run()
