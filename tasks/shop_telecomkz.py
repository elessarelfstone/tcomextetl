import datetime
import json
import os
from pathlib import Path

import luigi

from luigi.cmdline import luigi_run
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.extract.shop_telecomkz_requests import ShopTelecomKZApiParser
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import SHOP_TELECOMKZ_NURSAT_PLUS_TOKEN

host = 'https://shop.telecom.kz/api'


def calculate_progress(current_page, last_page):
    return int((current_page / last_page) * 100)


class ShopTelecomKzOutput(ApiToCsv):
    endpoint = luigi.Parameter()
    from_to = luigi.TupleParameter(default=())
    timeout = luigi.FloatParameter(default=5)
    token = luigi.Parameter(default=SHOP_TELECOMKZ_NURSAT_PLUS_TOKEN, visibility=ParameterVisibility.HIDDEN)

    @property
    def request_params(self):
        params = dict(page=1)

        # resume if there were fails
        if self.resume and os.path.exists(self.stat_fpath):
            next_page_params = self.stat['page_params']
            params.update(next_page_params)

        return params

    @property
    def params_for_stat(self):

        params = dict()
        params['from'], params['to'] = self.from_to

        return params

    def run(self):
        url = f'{host}{self.endpoint}'
        headers = dict()
        headers['Authorization'] = self.token

        parser = ShopTelecomKZApiParser(
            url,
            headers=headers,
            timeout=self.timeout,
            params=self.request_params
        )

        parser.set_parsed_count(self.stat.get('parsed', 0))

        for rows in parser:
            data = [dict_to_row(d, self.struct) for d in rows]
            save_csvrows(self.output_fpath, data, quotechar='"')
            self.set_status_info(*parser.status_percent)
            stat = parser.stat
            stat.update(self.params_for_stat)
            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(ShopTelecomKzOutput)
class ShopTelecomKzFtpOutput(FtpUploadedOutput):
    pass


class ShopTelecomKzRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())
    @property
    def params(self):
        params = super(ShopTelecomKzRunner, self).params
        params['from_to'] = (
            self.start_date.strftime(DEFAULT_FORMAT),
            self.end_date.strftime(DEFAULT_FORMAT)
        )
        return params

    def requires(self):
        return ShopTelecomKzFtpOutput(**self.params)


class ShopTelecomKzNursatPlus(ShopTelecomKzRunner):
    name = luigi.Parameter('shop_telecomkz_nursat_plus')


if __name__ == '__main__':
    code = luigi_run()
