import json
import os
from datetime import datetime
from time import sleep

import luigi

from luigi.util import requires
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import month_as_range, previous_month, yesterday, first_day_of_month, last_day_of_month, \
    DEFAULT_DATETIME_FORMAT
from tcomextetl.common.utils import read_lines, append_file, rewrite_file
from tcomextetl.extract.dgov_requests import DgovParser
from tasks.base import ApiToCsv, Runner, FtpUploadedOutput

headers = {'user-agent': 'Apache-HttpClient/4.1.1 (java 1.5)'}


class DgovDatasets(ApiToCsv):
    rep_name = luigi.Parameter()
    from_to = luigi.TupleParameter(default=())
    version = luigi.Parameter(default='v1')
    timeout = luigi.FloatParameter(default=2)

    def run(self):

        # create empty output file if no data
        super(ApiToCsv, self).run()

        chunks = None
        if os.path.exists(self.parsed_ids_fpath):
            chunks = read_lines(self.parsed_ids_fpath)

        params = None

        # specify period for updates
        if self.from_to:
            params = dict()
            params['from'] = self.from_to[0]
            params['to'] = self.from_to[1]

        parser = DgovParser(self.rep_name, self.version, params=params,
                            parsed_chunks=chunks, headers=headers)

        for data in parser:
            save_csvrows(self.output_fpath, [dict_to_row(d, self.struct) for d in data])
            self.set_status_info(*parser.status_percent)

            # log parsed chunks
            append_file(self.parsed_ids_fpath, parser.curr_chunk)
            sleep(self.timeout)

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(DgovDatasets)
class DgovDatasetsFtpOutput(FtpUploadedOutput):
    pass


class DgovDatasetsRunner(Runner):
    month = luigi.Parameter(default=previous_month())

    def requires(self):
        def date_as_datetime(dt):
            return datetime(year=dt.year, month=dt.month, day=dt.day).strftime('%Y-%m-%d %H:%M:%S')

        params = self.params
        if not self.all_data:
            from_to = month_as_range(self.month)
            params['from_to'] = (date_as_datetime(from_to[0]), date_as_datetime(from_to[1]))
        return DgovDatasetsFtpOutput(**params)


class DgovDatasetsPrivateSchools(DgovDatasetsRunner):
    name = luigi.Parameter('dgov_datasets_private_schools')



if __name__ == '__main__':
    luigi.run()
