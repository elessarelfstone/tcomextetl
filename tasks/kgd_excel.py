import luigi
from luigi.util import requires

from tcomextetl.common.dates import first_day_of_month
from tasks.base import Runner, FtpUploadedOutput
from tasks.xls import WebExcelFileParsingToCsv


class KgdExcelRunner(Runner):

    date = luigi.DateParameter(default=first_day_of_month())


class KgdBankruptOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdBankruptOutput)
class KgdBankruptFtpOutput(FtpUploadedOutput):
    pass


class KgdBankrupt(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_bankrupt')

    def requires(self):
        return KgdBankruptFtpOutput(**self.params)


class KgdInactiveOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdInactiveOutput)
class KgdInactiveFtpOutput(FtpUploadedOutput):
    pass


class KgdInactive(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_inactive')

    def requires(self):
        return KgdInactiveFtpOutput(**self.params)


class KgdInvregistrationOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdInvregistrationOutput)
class KgdInvregistrationFtpOutput(FtpUploadedOutput):
    pass


class KgdInvregistration(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_invregistration')

    def requires(self):
        return KgdInvregistrationFtpOutput(**self.params)


class KgdWrongAddressOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdWrongAddressOutput)
class KgdWrongAddressFtpOutput(FtpUploadedOutput):
    pass


class KgdWrongAddress(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_jwrongaddress')

    def requires(self):
        return KgdWrongAddressFtpOutput(**self.params)


class KgdPseudoCompanyOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdPseudoCompanyOutput)
class KgdPseudoCompanyFtpOutput(FtpUploadedOutput):
    pass


class KgdPseudoCompany(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_pseudocompany')

    def requires(self):
        return KgdPseudoCompanyFtpOutput(**self.params)


class KgdTaxArrears150Output(WebExcelFileParsingToCsv):
    pass


@requires(KgdTaxArrears150Output)
class KgdTaxArrears150FtpOutput(FtpUploadedOutput):
    pass


class KgdTaxArrears150(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_taxarrears150')

    def requires(self):
        return KgdTaxArrears150FtpOutput(**self.params)


class KgdTaxViolatorsOutput(WebExcelFileParsingToCsv):
    pass


@requires(KgdTaxViolatorsOutput)
class KgdTaxViolatorsFtpOutput(FtpUploadedOutput):
    pass


class KgdTaxViolators(KgdExcelRunner):

    name = luigi.Parameter(default='kgd_taxviolators')

    def requires(self):
        return KgdTaxViolatorsFtpOutput(**self.params)


if __name__ == '__main__':
    luigi.run()
