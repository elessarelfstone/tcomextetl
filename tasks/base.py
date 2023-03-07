import fnmatch
import gzip
import json
import logging
import os
import shutil
import tempfile
import traceback
from datetime import datetime, timedelta
from os.path import basename
from pathlib import Path
from shutil import move
from time import sleep

import luigi
from luigi.contrib.ftp import RemoteTarget, RemoteFileSystem
from luigi.parameter import ParameterVisibility
from luigi.util import requires


from settings import (DATA_PATH, TEMP_PATH, FTP_PATH, FTP_PASS,
                      FTP_HOST, FTP_USER, FTP_EXPORT_PATH, TBOT_TOKEN, TBOT_CHAT_IDS)

from tcomextetl.extract.http_requests import Downloader
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import CSV_DELIMITER
from tcomextetl.common.dates import DEFAULT_FORMAT, today
from tcomextetl.common.exceptions import FtpFileError
from tcomextetl.common.notify import send_message, send_document
from tcomextetl.common.utils import build_fpath, get_yaml_task_config, read_file
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
        self.downloader.download(p)


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
    resume = luigi.BoolParameter(default=False)  # use carefully

    @property
    def file_date(self):
        return '{date:%Y%m%d}'.format(date=self.date)

    def _file_path(self, ext):
        return build_fpath(self.directory, self.name,
                           ext, suff=self.file_date)

    @staticmethod
    def get_file_path(directory, name, ext, dt):
        return build_fpath(directory, name, ext, suff=dt)

    @property
    def output_fpath(self):
        return self._file_path(self.ext)

    def _clean(self):
        if os.path.exists(self.output_fpath):
            os.remove(self.output_fpath)

    def output(self):
        return luigi.LocalTarget(self.output_fpath)

    @property
    def success_fpath(self) -> str:
        return self._file_path('.scs')

    def run(self):
        open(self.output().path, 'a', encoding="utf-8").close()

    @property
    def params_for_report(self):
        return {"name": self.name, "date": self.date.strftime(DEFAULT_FORMAT)}


class ApiToCsv(CsvFileOutput):

    @property
    def stat_fpath(self) -> str:
        return self._file_path('.stat')

    @property
    def parsed_ids_fpath(self) -> str:
        return self._file_path('.prs')

    @property
    def stat(self) -> dict:
        if os.path.exists(self.stat_fpath):
            return json.loads(read_file(self.stat_fpath))
        else:
            return {}

    def _clean(self):

        super(ApiToCsv, self)._clean()

        if os.path.exists(self.parsed_ids_fpath):
            os.remove(self.parsed_ids_fpath)

        if os.path.exists(self.stat_fpath):
            os.remove(self.stat_fpath)

        if os.path.exists(self.success_fpath):
            os.remove(self.success_fpath)

    def finalize(self):
        if os.path.exists(self.stat_fpath):
            move(self.stat_fpath, self.success_fpath)

    def complete(self):
        if not os.path.exists(self.success_fpath):
            # start all over from scratch
            if not self.resume:
                # erase all the files we already have
                self._clean()

            return False
        else:
            return True

    def ids_to_parse(self, src_ids):
        if os.path.exists(self.parsed_ids_fpath):
            prs_ids = open(self.parsed_ids_fpath).readlines()


class FtpUploadedOutput(luigi.Task):

    ftp_directory = luigi.Parameter(default='')
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
    all_data = luigi.BoolParameter(default=False)
    date = luigi.DateParameter(default=today())
    resume = luigi.BoolParameter(default=True)

    @staticmethod
    def yesterday(frmt=DEFAULT_FORMAT):
        y = datetime.today() - timedelta(days=1)
        return y.strftime(frmt)

    @property
    def params(self) -> dict:
        """
        Load configuration as dict and return section according given name.
        """
        params_fpath = Path(__file__).parent.parent / 'tasks_params.yml'
        params = get_yaml_task_config(params_fpath, self.name)
        params['name'] = self.name
        params['date'] = self.date
        params['resume'] = self.resume
        return params

    @property
    def params_for_report(self) -> dict:
        params = self.params
        params['date'] = self.date.strftime(DEFAULT_FORMAT)

        _p = dict()
        _p['name'] = self.params['name']
        _p['date'] = self.params['date']
        t = CsvFileOutput(**_p)

        p = dict()

        if os.path.exists(t.success_fpath):
            p = json.loads(read_file(t.success_fpath))

        p['date'] = params['date']
        p["name"] = params["name"]

        f_path = build_fpath(TEMP_PATH, self.name, '.url')

        if os.path.exists(f_path):
            url = read_file(f_path)
            p["url"] = url

        return p


@Runner.event_handler(luigi.Event.SUCCESS)
def success_runner_handler(task):

    if (not TBOT_TOKEN) or (not TBOT_CHAT_IDS):
        return

    report = task.params_for_report
    task_name = report.pop('name')

    m = json.dumps(
        report,
        ensure_ascii=False,
        sort_keys=True,
        indent=2
    )

    chats = TBOT_CHAT_IDS.split(CSV_DELIMITER)
    chats = [int(chat_id) for chat_id in chats]

    message = f'✅ <b>{task_name}</b>\n<code>{m}</code>'
    send_message(TBOT_TOKEN, chats, message)


@CsvFileOutput.event_handler(luigi.Event.FAILURE)
def failure_runner_handler(task, exception):

    if (not TBOT_TOKEN) or (not TBOT_CHAT_IDS):
        return

    report = task.params_for_report
    caption = f'❌ <b>{report["name"]}</b>'
    suffix = f'_{report["name"]}_{report["date"]}_err.log'

    chats = TBOT_CHAT_IDS.split(CSV_DELIMITER)
    chats = [int(chat_id) for chat_id in chats ]

    try:
        f = tempfile.NamedTemporaryFile(suffix=suffix, mode='w', delete=False)
        f.write(traceback.format_exc())
        f_path = f.name
        f.close()
        send_document(TBOT_TOKEN, chats, caption, f_path)
    finally:
        os.unlink(f_path)


class ExternalFtpCsvDFInput(luigi.ExternalTask):

    ftp_file_mask = luigi.Parameter()

    @staticmethod
    def df_last_file(files):
        dates = []
        for f in files:
            fname = Path(f).stem
            _dt = fname.split('.')[0].split('_')[-2]
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
