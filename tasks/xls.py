import attr
import luigi
from luigi.util import requires

from tasks.base import CsvFileOutput, WebDataFileInput, ArchivedWebDataFileInput
from tcomextetl.common.excel import SimpleExcelDataReader
from tcomextetl.common.csv import save_csvrows


@requires(WebDataFileInput)
class WebExcelFileParsingToCsv(CsvFileOutput):

    skiptop = luigi.IntParameter(default=None)
    skipbottom = luigi.IntParameter(default=None)
    usecolumns = luigi.Parameter(default=None)
    sheets = luigi.Parameter(default=None)

    def run(self):
        super().run()
        xl = SimpleExcelDataReader(self.input().path, sheet_indexes=self.sheets,
                                   skip_rows=self.skiptop, use_cols=self.usecolumns)

        total = 0
        wrapper = self.struct

        for chunk in xl:
            # wrap in struct, transform
            rows = [attr.astuple(wrapper(*row)) for row in chunk]
            save_csvrows(self.output().path, rows)
            self.set_status_info(xl.status, xl.percent_done)


@requires(ArchivedWebDataFileInput)
class ArchivedWebExcelFileParsingToCsv(CsvFileOutput):

    skiptop = luigi.IntParameter(default=None)
    skipbottom = luigi.IntParameter(default=None)
    usecolumns = luigi.Parameter(default=None)
    sheets = luigi.Parameter(default=None)

    def run(self):
        super().run()
        for f_in in self.input():

            xl = SimpleExcelDataReader(f_in.path, sheet_indexes=self.sheets,
                                       skip_rows=self.skiptop, use_cols=self.usecolumns)

            total = 0
            wrapper = self.struct

            for chunk in xl:
                # wrap in struct, transform
                rows = [attr.astuple(wrapper(*row)) for row in chunk]
                save_csvrows(self.output().path, rows)
                self.set_status_info(xl.status, xl.percent_done)


