import pandas as pd
from math import floor
from pathlib import Path

from tcomextetl.common.utils import identify_file_format


class SimpleExcelDataReader:

    """ Parse data by reading Excel file sheet by sheet. """

    def __init__(
        self,
        excel_fpath: str,
        ws_indexes: list[int] = None,
        skip_rows: int = None,
        skip_footer: int = 0,
        use_cols: str = None,

    ):

        # parsed sheets and rows
        self._ws_parsed_cnt = 0
        self._parsed_cnt = 0

        self.excel_fpath = excel_fpath

        ext = Path(self.excel_fpath).suffix
        file_format = identify_file_format(excel_fpath)

        if ext == '.xlsx' and file_format == 'zip':
            engine = 'openpyxl'
        elif ext == '.xls' and file_format == 'xls':
            engine = 'xlrd'
        else:
            raise TypeError('Wrong format for Excel parsing.')

        self._ws_names = pd.ExcelFile(excel_fpath, engine=engine).sheet_names

        # read only specified sheets
        self._ws_indexes = ws_indexes

        if not ws_indexes:
            self._ws_indexes = [i for i, _ in enumerate(self._ws_names)]

        # number of rows to skip
        self._skip_rows = skip_rows
        self.skip_footer = skip_footer

        self.use_cols = use_cols

    @property
    def percent_done(self):
        total = len(self._ws_names)
        return floor((self._ws_parsed_cnt * 100) / total)

    @property
    def status(self):
        s = f'Total: {len(self._ws_names)}'
        s += f'Parsed: {self._parsed_cnt} rows, {self._ws_parsed_cnt} sheets.'
        return

    def __iter__(self):

        for sh_i in self._ws_indexes:
            df = pd.read_excel(
                self.excel_fpath,
                sheet_name=self._ws_names[sh_i],
                skiprows=self._skip_rows,
                skipfooter=self.skip_footer,
                usecols=self.use_cols,
                index_col=None,
                dtype=str,
                header=None,
                na_filter=False
                )

            self._ws_parsed_cnt += 1
            self._parsed_cnt += len(df.values)

            yield [tuple(r) for r in df.to_numpy().tolist()]
