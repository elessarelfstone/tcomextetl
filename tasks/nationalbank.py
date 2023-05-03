import luigi

from luigi.util import requires
from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from tcomextetl.extract.nb_requests import NbRatesParser
from tcomextetl.common.csv import save_csvrows


class NBRatesOutput(CsvFileOutput):

    def run(self):
        rates = NbRatesParser().get_rates()
        save_csvrows(self.output_fpath, rates)


@requires(NBRatesOutput)
class NBRatesFtpOutput(FtpUploadedOutput):
    pass


class NBRates(Runner):

    name = luigi.Parameter('nb_rates')

    def requires(self):
        return NBRatesFtpOutput(**self.params)


if __name__ == '__main__':
    luigi.run()




