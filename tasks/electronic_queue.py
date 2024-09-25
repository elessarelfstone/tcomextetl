import json
import os

import luigi

from luigi.cmdline import luigi_run
from tasks.base import ApiToCsv, FtpUploadedOutput, Runner
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.extract.electronic_queue_requests import ElectronicQueueApiParser
from tcomextetl.common.csv import dict_to_row, save_csvrows
from tcomextetl.common.dates import n_days_ago, DEFAULT_FORMAT
from tcomextetl.common.utils import rewrite_file
from settings import ELECTRONIC_QUEUE_LOGIN, ELECTRONIC_QUEUE_PASSWORD

url = 'http://10.8.27.158/serverterminal/hs/api-2/'


def calculate_progress(current, total):
    return int((current / total) * 100)


class ElectronicQueueOutput(ApiToCsv):
    from_to = luigi.TupleParameter(default=())
    timeout = luigi.FloatParameter(default=5)
    login = luigi.Parameter(default=ELECTRONIC_QUEUE_LOGIN, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=ELECTRONIC_QUEUE_PASSWORD, visibility=ParameterVisibility.HIDDEN)

    @property
    def request_params(self):
        params = dict()
        params['login'] = self.login
        params['password'] = self.password
        params['dateFrom'], params['dateTo'] = self.from_to

        return params

    def run(self):
        headers = {
            "Content-Type": "application/json"
        }
        print(self.request_params)
        parser = ElectronicQueueApiParser(
            url,
            headers=headers,
            timeout=self.timeout,
            data=self.request_params
        )

        rows = parser.load()
        if not rows:
            raise ExternalSourceError("Получен пустой ответ от API")
        data = []
        rows_count = 0
        for row in rows:
            try:
                # Преобразуем словарь в строку для CSV
                row_data = dict_to_row(row, self.struct)
                data.append(row_data)
                rows_count += 1
            except Exception as e:
                continue  # Пропускаем строки, которые не удалось обработать

        save_csvrows(self.output_fpath, data, quotechar='"')
        self.set_status_info(*parser.status_percent)
        stat = parser.stat
        stat.update({"parsed": rows_count})
        stat.update({"dateFrom-params": self.request_params['dateFrom']})
        stat.update({"dateTo-params": self.request_params['dateTo']})
        rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(ElectronicQueueOutput)
class ElectronicQueueFtpOutput(FtpUploadedOutput):
    pass


class ElectronicQueueRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(ElectronicQueueRunner, self).params
        params['from_to'] = (
            self.start_date.strftime("%Y-%m-%d 00:00:00"),
            self.end_date.strftime("%Y-%m-%d 23:59:59")
        )
        return params

    def requires(self):
        return ElectronicQueueFtpOutput(**self.params)


class ElectronicQueue(ElectronicQueueRunner):
    name = luigi.Parameter('electronic_queue')


if __name__ == '__main__':
    code = luigi_run()
