import attr
import json
import luigi
from luigi.util import requires

from tasks.base import CsvFileOutput, WebDataFileInput, ArchivedWebDataFileInput
from tcomextetl.common.excel import SimpleExcelDataReader
from tcomextetl.common.csv import save_csvrows
from tcomextetl.common.utils import rewrite_file


@requires(WebDataFileInput)
class WebExcelFileParsingToCsv(CsvFileOutput):

    skiptop = luigi.IntParameter(default=None)
    skipbottom = luigi.IntParameter(default=0)
    usecolumns = luigi.Parameter(default=None)
    sheets = luigi.Parameter(default=None)

    def run(self):
        super().run()
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
            rows = [attr.astuple(wrapper(*row)) for row in chunk]
            save_csvrows(self.output().path, rows)
            self.set_status_info(excel_reader.status, excel_reader.percent_done)

        rewrite_file(
            self.success_fpath,
            json.dumps(excel_reader.stat)
        )


@requires(ArchivedWebDataFileInput)
class ArchivedWebExcelFileParsingToCsv(CsvFileOutput):

    skiptop = luigi.IntParameter(default=None)
    skipbottom = luigi.IntParameter(default=0)
    usecolumns = luigi.Parameter(default=None)
    sheets = luigi.Parameter(default=None)

    def run(self):
        super().run()
        parsed_cnt = 0
        for f_in in self.input():

            excel_reader = SimpleExcelDataReader(
                f_in.path,
                ws_indexes=self.sheets,
                skip_rows=self.skiptop,
                skip_footer=self.skipbottom,
                use_cols=self.usecolumns,
                parsed_cnt=parsed_cnt
            )

            wrapper = self.struct
            for chunk in excel_reader:
                # wrap in struct, transform
                rows = [attr.astuple(wrapper(*row)) for row in chunk]
                save_csvrows(self.output().path, rows)
                parsed_cnt += len(rows)
                self.set_status_info(excel_reader.status, excel_reader.percent_done)

            rewrite_file(
                self.success_fpath,
                json.dumps(excel_reader.stat)
            )
