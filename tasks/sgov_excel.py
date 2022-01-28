import luigi
from luigi.util import requires

from tasks.base import Runner, FtpUploadedOutput
from tasks.xls import WebExcelFileParsingToCsv, ArchivedWebExcelFileParsingToCsv


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


if __name__ == '__main__':
    luigi.run()
