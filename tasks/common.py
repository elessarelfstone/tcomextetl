from datetime import datetime
from pathlib import Path


import luigi
import yaml
from luigi.contrib.ftp import RemoteTarget, RemoteFileSystem
from luigi.parameter import ParameterVisibility
from luigi.util import requires


from data_plugins.base import DotDict
from data_plugins.goszakup import GoszakupDataPlugin
from settings import DATA_PATH, FTP_PATH, FTP_HOST, FTP_USER, FTP_PASS, FTP_EXPORT_PATH


def file_path(
    directory: str,
    name: str,
    ext: str,
    suff: str = None
) -> Path:

    path = Path(directory) / '_'.join([name, suff]) if suff else name
    return path.absolute().with_suffix(ext)


class DataPluginRegister:

    _plugins = {}

    @classmethod
    def add(cls, name, plugin):
        cls._plugins[name] = plugin

    @classmethod
    def get(cls, name):
        try:
            return cls._plugins[name]
        except KeyError:
            raise ValueError(name)


DataPluginRegister.add('goszakup', GoszakupDataPlugin)


class CsvFtpOutput(luigi.Task):

    context = luigi.DictParameter(default={})

    @property
    def _context(self):
        return DotDict(self.context)

    @property
    def ftp_host(self):
        return self._context.ftp_host

    @property
    def ftp_creds(self):
        return dict(
            username=self._context.ftp_user,
            password=self._context.ftp_pass
        )

    @property
    def ftp_path(self):

        os_sep = self._context.os_sep
        root = self._context.ftp_path

        # use sep.join to avoid problems
        # with OS specific separator
        if self._context.ftp_directory:
            path = os_sep.join([root, self._context.ftp_directory])
        else:
            path = root

        return path

    @property
    def _output(self):
        """ Returns a list of files for uploading to FTP """
        def _name(file_name: str) -> str:

            if self._context.compress:
                return Path(file_name).with_suffix('.gzip').name
            else:
                return Path(file_name).name

        os_sep = self._context.os_sep

        return [os_sep.join([self.ftp_path, _name(f)]) for f in self._context.csv_files.values()]

    def output(self):
        return [RemoteTarget(f, self.ftp_host, **self.ftp_creds) for f in self._output]

    def run(self):
        # TODO implement
        pass


class CsvFtpRunner(luigi.WrapperTask):

    name = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.today())
    ext = luigi.Parameter(default='.csv')
    compress = luigi.BoolParameter(default=True)

    @property
    def file_date(self) -> str:
        """ Returns the run date in the YYYYMMDD format """
        return '{date:%Y%m%d}'.format(date=self.date)

    @property
    def ftp_config(self):
        return dict(
            ftp_host=FTP_HOST,
            ftp_user=FTP_USER,
            ftp_pass=FTP_PASS,
            ftp_path=FTP_PATH
        )

    def _file_path(
        self,
        directory: str,
        ext: str,
        suff: str = None
    ) -> Path:

        return file_path(
            directory=directory,
            name=self.name,
            ext=ext,
            suff=suff
        )

    @property
    def csv_fpath(self):
        return self._file_path(DATA_PATH, self.ext, self.file_date)

    @property
    def csv_files(self) -> dict:
        return dict(main=self.csv_fpath)

    def get_context(self) -> dict:
        """ Returns all the context needed for retrieval, validation, transformation, and upload """

        config_dir = Path(__file__).parent / 'config'
        config_fpath = self._file_path(config_dir, '.yml')

        # most of the context is stored in a yaml file
        # request parameters, data scheme, location on ftp, etc
        with open(config_fpath, 'r', encoding='utf-8') as file:
            config_context = yaml.safe_load(file)

        extra_context = dict(
            csv_files=self.csv_files,
            compress=self.compress,
            **self.ftp_config
        )

        return config_context | extra_context
