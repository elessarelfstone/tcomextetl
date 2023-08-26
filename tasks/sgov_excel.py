import csv
from datetime import datetime
from math import floor
from time import sleep

import attr
import json
import luigi
import pandas as pd
from luigi.util import requires

from tasks.base import Base, FtpUploadedOutput, Runner, CsvFileOutput
from tasks.xls import WebExcelFileParsingToCsv, ArchivedWebExcelFileParsingToCsv
from tcomextetl.extract.http_requests import Downloader
from tcomextetl.extract.sgov_requests import SgovApiRCutParser
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import CSV_QUOTECHAR
from tcomextetl.common.csv import save_csvrows
from tcomextetl.common.dates import first_day_of_month
from tcomextetl.common.excel import SimpleExcelDataReader
from tcomextetl.common.utils import build_fpath, append_file, read_file, rewrite_file
from settings import TEMP_PATH


rcut_legal_entities = 'legal_entities'
rcut_legal_branches = 'legal_branches'
rcut_joint_ventures = 'joint_ventures'
rcut_foreign_branches = 'foreign_branches'
rcut_entrepreneurs = 'entrepreneurs'


class SgovExcelRunner(Runner):

    date = luigi.DateParameter(default=first_day_of_month())
    resume = luigi.BoolParameter(default=False)


class SgovKatoOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovKatoOutput)
class SgovKatoFtpOutput(FtpUploadedOutput):
    pass


class SgovKato(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kato')

    def requires(self):
        return SgovKatoFtpOutput(**self.params)


# class SgovOkedOutput(WebExcelFileParsingToCsv):
#     pass


class SgovOkedOutput(WebExcelFileParsingToCsv):

    def run(self):

        # super().run()
        excel_reader = SimpleExcelDataReader(
            self.input().path,
            ws_indexes=self.sheets,
            skip_rows=self.skiptop,
            skip_footer=self.skipbottom,
            use_cols=self.usecolumns
        )

        wrapper = self.struct
        for chunk in excel_reader:
            # wrap in struct, transform
            rows = []
            for i, row in enumerate(chunk, start=1):
                _row = list(row)
                _row.append(str(i))
                _row = tuple(_row)
                rows.append(attr.astuple(wrapper(*_row)))

            save_csvrows(self.output().path, rows)
            self.set_status_info(excel_reader.status, excel_reader.percent_done)

        rewrite_file(
            self.success_fpath,
            json.dumps(excel_reader.stat)
        )


@requires(SgovOkedOutput)
class SgovOkedFtpOutput(FtpUploadedOutput):
    pass


class SgovOked(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_oked')

    def requires(self):
        return SgovOkedFtpOutput(**self.params)


class SgovMkeisOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovMkeisOutput)
class SgovMkeisFtpOutput(FtpUploadedOutput):
    pass


class SgovMkeis(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_mkeis')

    def requires(self):
        return SgovMkeisFtpOutput(**self.params)


class SgovKurkOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovKurkOutput)
class SgovKurkFtpOutput(FtpUploadedOutput):
    pass


class SgovKurk(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kurk')

    def requires(self):
        return SgovKurkFtpOutput(**self.params)


class SgovKpvedOutput(WebExcelFileParsingToCsv):
    pass


@requires(SgovKpvedOutput)
class SgovKpvedFtpOutput(FtpUploadedOutput):
    pass


class SgovKpved(SgovExcelRunner):

    name = luigi.Parameter(default='sgov_kpved')

    def requires(self):
        return SgovKpvedFtpOutput(**self.params)


class SgovRcutJuridicalLinkOutput(CsvFileOutput):

    juridical_type_id = luigi.IntParameter()
    statuses = luigi.ListParameter(default=[39354, 39355, 39356, 39358, 534829, 39359])
    prev_period_index = luigi.IntParameter(default=0)
    timeout = luigi.IntParameter(default=200)

    @staticmethod
    def build_fpath(name):
        return build_fpath(TEMP_PATH, name, '.url')

    def output(self):
        return luigi.LocalTarget(SgovRcutJuridicalLinkOutput.build_fpath(self.name))

    def run(self):
        p = SgovApiRCutParser(self.juridical_type_id, self.statuses, self.prev_period_index)

        order_id = p.place_order()

        status_info = f'OrderID : {order_id}. Waiting for url...'
        self.set_status_info(status_info, 50)

        url = None

        while url is None:
            sleep(self.timeout)
            url = p.check_state(order_id)

        append_file(self.output().path, url)
        status_info += '\n' + f' Url: {url}'
        self.set_status_info(status_info, 100)


class SgovRcutJuridicalLinkRunner(Runner):

    def requires(self):
        params = self.params
        params.pop('date')
        params.pop('skiptop')
        params.pop('ftp_directory')
        return SgovRcutJuridicalLinkOutput(**params)


class SgovRcutsPrepared(luigi.WrapperTask):

    def requires(self):
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_{rcut_entrepreneurs}')


class SgovRcutsActivePrepared(luigi.WrapperTask):

    def requires(self):
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_active_{rcut_legal_entities}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_active_{rcut_joint_ventures}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_active_{rcut_legal_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_active_{rcut_foreign_branches}')
        yield SgovRcutJuridicalLinkRunner(name=f'sgov_active_{rcut_entrepreneurs}')


class SgovRcutJuridicalOutput(ArchivedWebExcelFileParsingToCsv):
    pass


@requires(SgovRcutJuridicalOutput)
class SgovRcutJuridicalFtpOutput(FtpUploadedOutput):
    pass


class SgovRcutJuridicalRunner(Runner):

    date = luigi.DateParameter(default=datetime.today().replace(day=1).date())

    def requires(self):

        link_task_class = SgovRcutJuridicalLinkOutput

        params = self.params
        del params['juridical_type_id']
        del params['timeout']
        if params.get('statuses'):
            del params['statuses']
        # get prepared url
        params['url'] = read_file(link_task_class.build_fpath(self.name))
        params['wildcard'] = '*.xlsx'

        return SgovRcutJuridicalFtpOutput(**params)


class SgovRcutsJuridical(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_{rcut_entrepreneurs}')


class SgovRcutsActiveJuridical(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutJuridicalRunner(name=f'sgov_active_{rcut_legal_entities}')
        yield SgovRcutJuridicalRunner(name=f'sgov_active_{rcut_joint_ventures}')
        yield SgovRcutJuridicalRunner(name=f'sgov_active_{rcut_legal_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_active_{rcut_foreign_branches}')
        yield SgovRcutJuridicalRunner(name=f'sgov_active_{rcut_entrepreneurs}')


class SgovRcutByKatoJuridicalOutput(CsvFileOutput):

    juridical_type_id = luigi.IntParameter()
    skiptop = luigi.IntParameter(default=None)
    skipbottom = luigi.IntParameter(default=0)
    usecolumns = luigi.Parameter(default=None)
    sheets = luigi.Parameter(default=None)
    statuses = luigi.ListParameter(default=[39354, 39355, 39356, 39358, 534829, 39359])
    kato_ids = luigi.ListParameter(default=[77208141, 247783, 248875, 250502, 252311, 253160, 255577, 77208139, 256619, 258742, 260099, 260907, 263009, 264023, 20243032, 77208140, 264990])
    # kato_ids = luigi.ListParameter(default=[77208141, 247783, 248875])
    prev_period_index = luigi.IntParameter(default=0)
    timeout = luigi.IntParameter(default=200)

    def run(self):

        urls = []
        # 1 step - getting urls
        for kato in self.kato_ids:

            p = SgovApiRCutParser(
                self.juridical_type_id,
                self.statuses,
                kato_id=kato,
                which_last=self.prev_period_index
            )

            order_id = p.place_order()

            status_info = f'OrderID : {order_id}. Kato: {kato}. Waiting for url...'
            self.set_status_info(status_info, 50)

            url = None

            while url is None:
                sleep(self.timeout)
                url = p.check_state(order_id)

            f_path = build_fpath(TEMP_PATH, f'{self.name}_{kato}', '.url')
            # file_paths.append(f_path)
            urls.append(url)

        # 2 step - gather data
        df = pd.DataFrame()
        row_count = 0

        for i, u in enumerate(urls, start=1):
            d = Downloader(u)
            a_fpath = build_fpath(TEMP_PATH, f'{self.name}_{kato}', '.zip')
            d.download(a_fpath)
            f_path, *_ = extract_by_wildcard(a_fpath, wildcard='*.xlsx')

            excel_reader = SimpleExcelDataReader(
                f_path,
                ws_indexes=self.sheets,
                skip_rows=self.skiptop,
                skip_footer=self.skipbottom,
                use_cols=self.usecolumns
            )

            wrapper = self.struct
            for chunk in excel_reader:
                # wrap in struct, transform
                rows = [attr.astuple(wrapper(*row)) for row in chunk]
                save_csvrows(self.output_fpath, rows)
                row_count += len(rows)
                self.set_status_info(excel_reader.status, excel_reader.percent_done)

        stat = {'parsed': row_count}
        append_file(self.success_fpath, json.dumps(stat))


@requires(SgovRcutByKatoJuridicalOutput)
class SgovRcutByKatoJuridicalFtpOutput(FtpUploadedOutput):
    pass


class SgovRcutByKatoJuridicalRunner(Runner):

    name = luigi.Parameter()
    date = luigi.DateParameter(default=datetime.today().replace(day=1).date())

    @property
    def params(self):
        params = super(SgovRcutByKatoJuridicalRunner, self).params
        return params

    def requires(self):
        return SgovRcutByKatoJuridicalFtpOutput(**self.params)


class SgovRcutByKatoJuridical(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_{rcut_legal_entities}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_{rcut_joint_ventures}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_{rcut_legal_branches}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_{rcut_foreign_branches}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_{rcut_entrepreneurs}')


class SgovRcutByKatoActiveJuridical(luigi.WrapperTask):
    def requires(self):
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_active_{rcut_legal_entities}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_active_{rcut_joint_ventures}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_active_{rcut_legal_branches}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_active_{rcut_foreign_branches}')
        yield SgovRcutByKatoJuridicalRunner(name=f'sgov_active_{rcut_entrepreneurs}')


if __name__ == '__main__':
    luigi.run()
