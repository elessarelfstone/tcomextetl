import gzip
import os
import shutil
from datetime import datetime
from pathlib import Path
from shutil import move
from time import sleep

import luigi
from luigi.contrib.ftp import RemoteTarget
from luigi.parameter import ParameterVisibility
from luigi.util import requires


from settings import (DATA_PATH, TEMP_PATH, FTP_PATH,
                      FTP_PASS, FTP_HOST, FTP_USER)

from tcomextetl.extract.http_requests import Downloader
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.dates import yesterday
from tcomextetl.common.utils import build_fpath, get_yaml_task_config
from tcomextetl.transform import StructRegister


class Base(luigi.Task):

    name = luigi.Parameter()
    descr = luigi.Parameter(default='')

    def set_status_info(self, status: str, percent: int = 0):
        self.set_status_message(status)
        self.set_progress_percentage(percent)

    @property
    def struct(self):
        return StructRegister.get(self.name)


class WebDataFileInput(Base):

    url = luigi.Parameter()
    _downloader = None

    @property
    def downloader(self):
        if self._downloader is None:
            self._downloader = Downloader(self.url)
        return self._downloader

    def output(self):
        f_path = build_fpath(TEMP_PATH, self.name, f'.{self.downloader.ext}')
        return luigi.LocalTarget(f_path)

    @property
    def status(self):
        return f'Saving in {self.output().path}' + '\n'

    def run(self):
        p = self.output().path
        with open(p, 'wb') as f:
            for ch in self.downloader:
                f.write(ch)
                self.set_status_info(self.status + self.downloader.status)


@requires(WebDataFileInput)
class ArchivedWebDataFileInput(luigi.Task):

    wildcard = luigi.Parameter(default='*.xlsx')
    files_count = luigi.IntParameter(default=1)

    @property
    def file_paths(self):
        ext = self.wildcard[1:]
        cnt = self.files_count
        return [build_fpath(TEMP_PATH, f'{self.name}_{i}', ext) for i in range(cnt)]

    def output(self):
        sleep(0.5)
        return [luigi.LocalTarget(f) for f in self.file_paths]

    def run(self):
        arch_fpath = self.input().path
        e_paths = extract_by_wildcard(arch_fpath, wildcard=self.wildcard)

        # rename extracted files to have understandable names
        for i, e_path in enumerate(e_paths):
            move(e_path, self.file_paths[i])


class CsvFileOutput(Base):
    date = luigi.DateParameter(default=datetime.today(), visibility=ParameterVisibility.HIDDEN)
    directory = luigi.Parameter(default=DATA_PATH, visibility=ParameterVisibility.HIDDEN)
    ext = luigi.Parameter(default='.csv', visibility=ParameterVisibility.HIDDEN)
    sep = luigi.Parameter(default=';', visibility=ParameterVisibility.HIDDEN)

    @property
    def file_date(self):
        return '{date:%Y%m%d}'.format(date=self.date)

    def _file_path(self, ext):
        return build_fpath(self.directory, self.name,
                           ext, suff=self.file_date)

    @property
    def output_path(self):
        return self._file_path(self.ext)

    def output(self):
        return luigi.LocalTarget(self.output_path)


class ApiToCsv(CsvFileOutput):

    @property
    def meta_file_path(self):
        return self._file_path('.meta')

    @property
    def success_file_path(self):
        return self._file_path('.scs')

    @property
    def parsed_ids_file_path(self):
        return self._file_path('.prs')

    # @property
    # def params(self):
    #     return {}

    def complete(self):
        if not os.path.exists(self.success_file_path):
            return False
        else:
            return True


class FtpUploadedOutput(luigi.Task):

    ftp_directory = luigi.Parameter(default=None)

    gzip_ext = luigi.Parameter(default='.gzip')

    ftp_host = luigi.Parameter(default=FTP_HOST, visibility=ParameterVisibility.HIDDEN)
    ftp_user = luigi.Parameter(default=FTP_USER, visibility=ParameterVisibility.HIDDEN)
    ftp_pass = luigi.Parameter(default=FTP_PASS, visibility=ParameterVisibility.HIDDEN)
    ftp_path = luigi.Parameter(default=FTP_PATH, visibility=ParameterVisibility.HIDDEN)
    ftp_os_sep = luigi.Parameter(default='/', visibility=ParameterVisibility.HIDDEN)

    @property
    def gzip_fname(self):
        p = Path(self.input().path)
        return p.with_suffix(p.suffix + self.gzip_ext).name

    def gzip(self):

        gzip_fpath = os.path.join(os.path.dirname(os.path.abspath(self.input().path)),
                                  self.gzip_fname)

        with open(self.input().path, 'rb') as src:
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

        ftp_fpath = os_sep.join([path, self.gzip_fname])
        return RemoteTarget(ftp_fpath, self.ftp_host,
                            username=self.ftp_user, password=self.ftp_pass)

    def run(self):
        fpath = self.gzip()
        self.output().put(fpath, atomic=False)


class Runner(luigi.WrapperTask):
    """
    Base class for tasks which are supposed only to prepare
    all input parameters and run tasks with main functionality.
    """
    name = luigi.Parameter()
    period = luigi.Parameter(default='all')
    date = luigi.DateParameter(default=datetime.today())

    @property
    def yesterday(self):
        return yesterday()

    @property
    def params(self):
        """
            Load configuration as dict and return section according given name.
        """
        params = get_yaml_task_config(self.name)
        params['name'] = self.name
        params['date'] = self.date
        return params
