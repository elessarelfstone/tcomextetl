from pathlib import Path


import luigi
from luigi.contrib.ftp import RemoteTarget, RemoteFileSystem
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from data_plugins.base import FlattenedDict
from data_plugins.goszakup import GoszakupDataPlugin
from settings import DATA_PATH


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

    @staticmethod
    def _build_fpath(file_name: str) -> Path:
        path = Path(DATA_PATH) / file_name
        return path.absolute()

    @property
    def ftp_host(self):
        _context = FlattenedDict()(self.context)
        return _context.ftp_host

    @property
    def ftp_creds(self):
        _context = FlattenedDict()(self.context)
        return {'username': _context.ftp_host, 'password': _context.ftp_pass}

    def output(self):

        def gzip_name(file_name: str) -> str:
            p = Path(file_name)
            return p.with_suffix(p.suffix + '.gzip').name

        _context = FlattenedDict()(self.context)

        os_sep = _context.os_sep
        root = _context.ftp_path

        # use str.sep.join to avoid problems
        # OS specific separator
        if _context.ftp_directory:
            path = os_sep.join([root, _context.ftp_directory])
        else:
            path = root

        # TODO done building ftp path
        return [RemoteTarget(self._build_fpath(f), self.ftp_host, **self.ftp_creds) for f in _context.files]

    def run(self):
        # TODO implement
        pass

        plugin = Plugin()






