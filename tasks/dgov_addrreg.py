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

        # create empty output file if no data
        super(ApiToCsv, self).run()

        chunks = None
        if os.path.exists(self.parsed_ids_file_path):
            chunks = read_lines(self.parsed_ids_file_path)

        params = None

        # specify period for updates
        if self.from_to:
            params = dict()
            params['from'] = self.from_to[0]
            params['to'] = self.from_to[1]

        parser = DgovParser(self.rep_name, self.version, params=params,
                            parsed_chunks=chunks, headers=headers)

        for data in parser:
            save_csvrows(self.output_path, [dict_to_csvrow(d, self.struct) for d in data])
            self.set_status_info(*parser.status_percent)

            # log parsed chunks
            append_file(self.parsed_ids_file_path, parser.curr_chunk)
            sleep(self.timeout)

        rewrite_file(self.success_file_path, parser.status_percent[0])


@requires(DgovAddrRegOutput)
class DgovAddrRegFtpOutput(FtpUploadedOutput):
    pass


class DgovAddrRegRunner(Runner):

    month = luigi.Parameter(default=previous_month())

    def requires(self):
        def date_as_datetime(dt):
            return datetime(year=dt.year, month=dt.month, day=dt.day).strftime('%Y-%m-%d %H:%M:%S')

        params = self.params
        if self.period == 'month':
            from_to = month_as_range(self.month)
            params['from_to'] = (date_as_datetime(from_to[0]), date_as_datetime(from_to[1]))
        return DgovAddrRegFtpOutput(**params)


class DgovAddrRegSPb(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_spb')


class DgovAddrRegSAts(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_sats')


class DgovAddrRegSGeonims(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_sgeonims')


class DgovAddrRegSGrounds(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_sgrounds')


class DgovAddrRegSBuildings(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_sbuildings')


class DgovAddrRegDAtsTypes(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_dats_types')


class DgovAddrRegDBuildingsPointers(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_dbuildings_pointers')


class DgovAddrRegDGeonimsTypes(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_dgeonims_types')


class DgovAddrRegDRoomsTypes(DgovAddrRegRunner):

    name = luigi.Parameter('dgov_addrreg_drooms_types')


if __name__ == '__main__':
    luigi.run()
