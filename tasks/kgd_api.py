import gzip
import os
import shutil
from collections import deque
from datetime import datetime, timedelta
from math import floor
from pathlib import Path
from time import sleep

import luigi
from luigi.contrib.ftp import RemoteTarget
from luigi.util import requires

from tasks.base import Runner, ApiToCsv, ExternalFtpCsvDFInput, FtpUploadedOutput
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import previous_month, month_as_range
from tcomextetl.common.utils import append_file, rewrite_file, read_file, read_lines, build_fpath
from tcomextetl.extract.kgd_requests import (KgdGovKzSoapApiParser, KgdGovKzSoapApiError,
                                             KgdGovKzSoapApiResponseError, KgdGovKzSoapApiNotAvailable)

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
    def total(self):
        return self._source_bins_count

    @property
    def parsed(self):
        return self._parsed_bins_count

    def status_info(self, bid, stat=None):
        s = f'Total: {self._source_bins_count}. Parsed: {self._parsed_bins_count}.' + '\n'
        s += f'Parsing payments on {bid} in {self.output_fpath}.' + '\n'
        s += stat
        return s


class KgdSoapApiTaxPaymentOutput(ApiToCsv):

    start_date = luigi.Parameter()
    end_date = luigi.Parameter()
    ftp_file_mask = luigi.Parameter()
    timeout = luigi.FloatParameter(default=1.5)
    timeout_ban = luigi.FloatParameter(default=5)
    notaxes_fext = luigi.Parameter('.notaxes')

    @property
    def url(self):
        return url_template.format(KGD_SOAP_TOKEN)

    @property
    def request_form(self):
        r_form_fpath = Path(__file__).parent.parent / 'misc' / 'kgd' / 'tax_payments_request_form.xml'
        return read_file(r_form_fpath)

    @property
    def bins_fpath(self):
        return build_fpath(self.directory, self.name, '.bins')

    @property
    def failed_fpath(self):
        return self._file_path('.failed')

    @property
    def notaxes_fpath(self):
        return self._file_path(self.notaxes_fext)

    def requires(self):
        return ExternalFtpCsvDFInput(ftp_file_mask=self.ftp_file_mask)

    def output(self):
        return [luigi.LocalTarget(self.parsed_ids_fpath),
                luigi.LocalTarget(self.notaxes_fpath),
                super().output()
                ]

    # TODO add complete method

    def run(self):
        # get bins
        if not os.path.exists(self.bins_fpath):
            self.input().get(str(self.bins_fpath))

        params = {'begin_date': self.start_date, 'end_date': self.end_date}
        parser = KgdGovKzSoapApiParser(
            self.url,
            self.request_form,
            params=params,
            headers=headers
        )

        bins_manager = BinsManager(
            self.bins_fpath,
            self.output_fpath,
            self.parsed_ids_fpath
        )

        bins = bins_manager.bins
        failed_bins = deque()
        parsed_cnt = bins_manager.parsed
        while bins:

            if failed_bins:
                _bin = failed_bins.popleft()
            else:
                _bin = bins.popleft()

            try:

                payments = parser.process_bin(_bin)

            except KgdGovKzSoapApiResponseError as e:
                failed_bins.append(_bin)
                sleep(self.timeout)
            except KgdGovKzSoapApiError as e:
                append_file(self.parsed_ids_fpath, _bin)
                parsed_cnt += 1
                if str(e).endswith('10'):
                    append_file(self.notaxes_fpath, _bin)
                sleep(self.timeout)
            except KgdGovKzSoapApiNotAvailable:
                if not parser.is_server_up:
                    print('Server is not available.')
                    exit()
                else:
                    failed_bins.append(_bin)
                    sleep(self.timeout_ban)

            except Exception as e:
                raise

            else:
                data = []
                for p in payments:
                    row = dict_to_row(p, self.struct)
                    data.append(row)

                if data:
                    save_csvrows(self.output_fpath, data)

                append_file(self.parsed_ids_fpath, _bin)
                parsed_cnt += 1

            s = f'Total: {bins_manager.total}. Parsed: {parsed_cnt}. BIN: {_bin}' + '\n'
            rewrite_file(self.stat_fpath, s + parser.stat_meta_info)

            p = floor((parsed_cnt * 100) / bins_manager.total)
            self.set_status_info(s + parser.stat_meta_info, p)

        self.finalize()


@requires(KgdSoapApiTaxPaymentOutput)
class KgdSoapApiTaxPaymentFtpUploadedOutput(FtpUploadedOutput):

    def file_name(self, input_fpath):
        tomorrow = datetime.today() + timedelta(days=1)
        suff_tomorrow = '{date:%Y%m%d}'.format(date=tomorrow)
        ext = Path(input_fpath).suffix

        # have to break it down to pieces to get file name without date
        pieces = Path(input_fpath).stem.split('_')
        pieces.pop()
        pieces.append(suff_tomorrow)
        f_name = '_'.join(pieces)
        return Path(f_name).with_suffix(ext + self.gzip_ext).name

    def gzip_file(self, input_fpath):

        gzip_fpath = os.path.join(os.path.dirname(os.path.abspath(input_fpath)),
                                  self.file_name(input_fpath))

        with open(input_fpath, 'rb') as src:
            with gzip.open(gzip_fpath, 'wb') as dest:
                shutil.copyfileobj(src, dest)

        return gzip_fpath

    def output(self):

        os_sep = str(self.ftp_os_sep)
        root = self.ftp_path

        # use str.sep.join to avoid problems
        # OS specific separator
        if self.ftp_directory:
            path = os_sep.join([root, self.ftp_directory])
        else:
            path = root

        ftp_remote_targets = []
        for fi in self.input():
            ftp_fpath = os_sep.join([path, self.file_name(fi.path)])
            ftp_remote_targets.append(RemoteTarget(ftp_fpath, self.ftp_host,
                                                   username=self.ftp_user, password=self.ftp_pass))

        return ftp_remote_targets

    def run(self):
        for i, fi in enumerate(self.input()):
            fpath = self.gzip_file(fi.path)
            self.output()[i].put(fpath, atomic=False)


class KgdSoapApiTaxPayments(Runner):

    name = luigi.Parameter(default='kgd_taxpayments')
    month = luigi.Parameter(default=previous_month())
    date = luigi.Parameter(default=datetime.today().replace(day=1).date())

    def requires(self):
        begin_date, end_date = month_as_range(self.month)
        return KgdSoapApiTaxPaymentFtpUploadedOutput(
            begin_date=begin_date,
            end_date=end_date,
            **self.params
        )


if __name__ == '__main__':
    luigi.run()
