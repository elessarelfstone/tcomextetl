import os
from collections import deque

import luigi

from tasks.base import ApiToCsv, ExternalFtpCsvDFInput
from tcomextetl.common.utils import read_file, read_lines, build_fpath
from tcomextetl.extract.kgdgov_requests import KgdGovKzSoapApiParser

from settings import KGD_SOAP_TOKEN


url_template = "https://open.egov.kz/proxy2/culs_payments?token={}"
headers = {'user-agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
           'content-type': 'text/xml'}


class BinsManager:
    def __init__(self, bins_fpath, output_fpath, parsed_fpath):
        self.failed_bins = deque([])
        self.output_fpath = output_fpath

        parsed_bins = []
        if os.path.exists(parsed_fpath):
            parsed_bins = read_lines(parsed_fpath)

        self._parsed_bins_count = len(parsed_bins)

        source_bins = [bn for bn in read_lines(bins_fpath) if BinsManager.check_bin(bn)]
        self._source_bins_count = len(source_bins)

        # excluding parsed bids
        if parsed_bins:
            s = set(source_bins)
            s.difference_update(set(parsed_bins))
            self.bins = deque(list(s))
        else:
            self.bins = deque(source_bins)

    @staticmethod
    def check_bin(bn):
        if len(bn) != 12:
            return False
        else:
            return all([c.isdigit() for c in bn])

    @property
    def source_bids_count(self):
        return self._source_bins_count

    @property
    def parsed_bids_count(self):
        return self._parsed_bins_count

    def status_info(self, bid, is_reprocess=False, stat=None):
        r = 'Reprocessing' if is_reprocess else ''
        s = f'Total: {self.source_bids_count}. Parsed: {self.parsed_bids_count}.' + '\n'
        s += f'Parsing payments on {bid} in {self.output_fpath}. {r}' + '\n'
        s += stat
        return s


class KgdSoapApiTaxPaymentOutput(ApiToCsv):

    start_date = luigi.Parameter()
    end_date = luigi.Parameter()
    timeout = luigi.FloatParameter(default=1.5)
    notaxes_fext = luigi.Parameter('notaxes')

    @property
    def bins_fpath(self):
        return build_fpath(self.directory, self.name, 'bins')

    @property
    def notaxes_fpath(self):
        return build_fpath(self.directory, self.name, self.notaxes_fext)

    def requires(self):
        return ExternalFtpCsvDFInput(ftp_file_mask='export_kgdgovkz_bins_*.csv')

    def output(self):
        return [luigi.LocalTarget(self.parsed_ids_file_path),
                luigi.LocalTarget(self.notaxes_fpath),
                super().output()
                ]

    def run(self):
        # get bins
        if not os.path.exists(self.bins_fpath):
            self.input().get(self.bins_fpath)

        url = url_template.format(KGD_SOAP_TOKEN)
        r_form = read_file()
        parser = KgdGovKzSoapApiParser(url, r_form)

        bins_queue = BinsManager(self.bins_fpath, self.output_path,
                                 self.parsed_ids_file_path)

        while bins_queue:


























