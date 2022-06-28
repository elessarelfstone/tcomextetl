import os
from datetime import datetime
from time import sleep

import luigi

from luigi.util import requires
from tcomextetl.common.csv import dict_to_csvrow, save_csvrows
from tcomextetl.common.dates import month_as_range, previous_month, yesterday
from tcomextetl.common.utils import read_lines, append_file, rewrite_file
from tcomextetl.extract.dgov_requests import DgovParser
from tasks.base import ApiToCsv, Runner, FtpUploadedOutput

headers = {'user-agent': 'Apache-HttpClient/4.1.1 (java 1.5)'}


class DgovAddrRegOutput(ApiToCsv):

    rep_name = luigi.Parameter()
    from_to = luigi.TupleParameter(default=())
    version = luigi.Parameter(default='data')
    timeout = luigi.FloatParameter(default=2)

    def run(self):
        chunks = None
        if os.path.exists(self.parsed_ids_file_path):
            chunks = read_lines(self.parsed_ids_file_path)

        params = None

        if self.from_to:
            params = dict()
            params['from'] = self.from_to[0]
            params['to'] = self.from_to[1]

        parser = DgovParser(self.rep_name, self.version, params=params,
                            parsed_chunks=chunks, headers=headers)

        for dicts in parser:
            data = [dict_to_csvrow(d, self.struct) for d in dicts]
            save_csvrows(self.output_path, data)
            self.set_status_info(*parser.status_percent)
            append_file(self.parsed_ids_file_path, parser.curr_chunk)
            sleep(self.timeout)

        rewrite_file(self.success_file_path, parser.status_percent[0])


@requires(DgovAddrRegOutput)
class DgovAddrRegFtpOutput(FtpUploadedOutput):
    pass


class DgovAddrRegPrevMonthRunner(Runner):

    month = luigi.Parameter(default=previous_month())

    def requires(self):
        params = self.params
        if self.period == 'month':
            from_to = month_as_range(self.month)
            f = from_to[0]
            t = from_to[1]
            f = datetime(year=f.year, month=f.month, day=f.day).strftime('%Y-%m-%d %H:%M:%S')
            t = datetime(year=t.year, month=t.month, day=t.day).strftime('%Y-%m-%d %H:%M:%S')
            params['from_to'] = (f, t)
        return DgovAddrRegFtpOutput(**params)


class DgovAddrregSpb(DgovAddrRegPrevMonthRunner):

    name = luigi.Parameter('dgov_addrreg_spb')


if __name__ == '__main__':
    luigi.run()
