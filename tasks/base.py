import fnmatch
import gzip
import os
import shutil
import sys
from datetime import datetime, timedelta
from os.path import basename
from pathlib import Path
from shutil import move
from time import sleep

import luigi
from luigi.contrib.ftp import RemoteTarget, RemoteFileSystem
from luigi.parameter import ParameterVisibility
from luigi.util import requires


from settings import (DATA_PATH, TEMP_PATH, FTP_PATH,
                      FTP_PASS, FTP_HOST, FTP_USER, FTP_EXPORT_PATH)

from tcomextetl.extract.http_requests import Downloader
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.dates import DEFAULT_FORMAT
from tcomextetl.common.exceptions import FtpFileError
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

    @luigi.Task.event_handler(luigi.Event.FAILURE)
    def exit_message(self):
        sys.exit(40)


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

    def run(self):
        open(self.output().path, 'a', encoding="utf-8").close()


class ApiToCsv(CsvFileOutput):

    @property
    def stat_file_path(self):
        return self._file_path('.stat')

    @property
    def success_file_path(self):
        return self._file_path('.scs')

    @property
    def parsed_ids_file_path(self):
        return self._file_path('.prs')

    def finalize(self):
        if os.path.exists(self.stat_file_path):
            move(self.stat_file_path, self.success_file_path)

    def complete(self):
        if not os.path.exists(self.success_file_path):
            return False
        else:
            return True

    def ids_to_parse(self, src_ids):
        if os.path.exists(self.parsed_ids_file_path):
            prs_ids = open(self.parsed_ids_file_path).readlines()


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
    period = luigi.Parameter(default='interval')
    date = luigi.DateParameter(default=datetime.today())

    @staticmethod
    def yesterday(frmt=DEFAULT_FORMAT):
        y = datetime.today() - timedelta(days=1)
        return y.strftime(frmt)

    @property
    def params(self):
        """
            Load configuration as dict and return section according given name.
        """
        params_fpath = Path(__file__).parent.parent / 'tasks_params.yml'
        params = get_yaml_task_config(params_fpath, self.name)
        params['name'] = self.name
        params['date'] = self.date
        return params


class ExternalFtpCsvDFInput(luigi.ExternalTask):

    ftp_file_mask = luigi.Parameter()

    @staticmethod
    def df_last_file(files):
        dates = []
        for f in files:
            fname = Path(f).stem
            _dt = fname.split('_')[3]
            dt = datetime.strptime(_dt, '%Y-%m-%d')
            dates.append((dt, f))

        dates.sort(key=lambda x: x[1])

        return dates[-1][1]

    def output(self):

        rmfs = RemoteFileSystem(FTP_HOST, username=FTP_USER, password=FTP_PASS)

        files = None

        if rmfs.exists(FTP_EXPORT_PATH):
            files = rmfs.listdir(FTP_EXPORT_PATH)
            files = fnmatch.filter([basename(f) for f in files], self.ftp_file_mask)
        else:
            raise FtpFileError('Could not find directory')

        if not files:
            raise FtpFileError('Could not find any file')

        bins_fpath = FTP_EXPORT_PATH + '/' + ExternalFtpCsvDFInput.df_last_file(files)
        return RemoteTarget(bins_fpath, FTP_HOST,
                            username=FTP_USER, password=FTP_PASS)


class ExternalCsvLocalInput(luigi.ExternalTask):

    name = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.today(), visibility=ParameterVisibility.HIDDEN)
    directory = luigi.Parameter(default=DATA_PATH, visibility=ParameterVisibility.HIDDEN)
    ext = luigi.Parameter(default='.csv', visibility=ParameterVisibility.HIDDEN)
    sep = luigi.Parameter(default=';', visibility=ParameterVisibility.HIDDEN)

    def output(self):
        fpath = build_fpath(self.directory, self.name, self.ext,
                            suff='{date:%Y%m%d}'.format(date=self.date))

        return luigi.LocalTarget(fpath)

