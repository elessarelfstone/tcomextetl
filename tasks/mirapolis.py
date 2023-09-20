import json
import hashlib
from urllib import parse

import luigi

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.mirapolis_requests import MirapolisRequests
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import MIRAPOLIS_SECRET_KEY


url_templ = 'https://learning.telecom.kz/mira/service/v2/reportTemplates/{}/report/json'


class MirapolisOutput(CsvFileOutput):

    report_id = luigi.IntParameter()
    report_group_id = luigi.IntParameter()
    from_to = luigi.TupleParameter(default=())
    secret_key = luigi.Parameter(default=MIRAPOLIS_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)

    @property
    def request_params(self):

        from_templ = '{} 00:00:00.000'
        to_templ = '{} 23:59:59.000'
        params = dict()
        params['param1'] = from_templ.format(self.from_to[0])
        params['param2'] = to_templ.format(self.from_to[1])
        params['param3'] = self.report_group_id
        params['appid'] = 'system'

        key_value_pairs = []
        for key, value in params.items():
            key_value_pairs.append(f"{key}={value}")

        query_string = "&".join(key_value_pairs)

        _url_templ = url_templ.format(self.report_id) + '?' + query_string + '&{}'
        _hash = hashlib.md5(_url_templ.format("secretkey=hg&9iskK").encode()).hexdigest().upper()
        url = _url_templ.format(f"sign={_hash}")
        params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        return params

    def run(self):

        parser = MirapolisRequests(
            url_templ,
            self.report_id,
            params=self.request_params
        )
        row_count = 0
        buffer = []
        for d in parser:
            buffer.append(self.struct.from_raw(d))
            save_csvrows(self.output_fpath, [dict_to_row(d, self.struct) for d in buffer])
            buffer.clear()
            row_count += 1

        stat = parser.stat
        # stat.update(json_body)
        stat.update({'parsed': row_count})
        rewrite_file(self.success_fpath, json.dumps(stat))


@requires(MirapolisOutput)
class MirapolisOutputFtpOutput(FtpUploadedOutput):
    pass


class MirapolisRunner(Runner):

    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(MirapolisRunner, self).params

        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return MirapolisOutputFtpOutput(**self.params)


class MirapolisOffline(MirapolisRunner):

    name = luigi.Parameter('mirapolis_offline_study')


class MirapolisOnline(MirapolisRunner):

    name = luigi.Parameter('mirapolis_online_study')


if __name__ == '__main__':
    code = luigi.run()
