import numpy as np
import pandas as pd
from math import floor
from pathlib import Path

from tcomextetl.common.utils import identify_file_format


class SimpleExcelDataReader:

    """ Parse data by reading Excel file sheet by sheet. """

    def __init__(self, excel_fpath, sheet_indexes=None,
                 skip_rows=None, use_cols=None):

        self.parsed_sheets = 0
        self.parsed_rows = 0

        self.excel_fpath = excel_fpath

        ext = Path(self.excel_fpath).suffix
        file_format = identify_file_format(excel_fpath)

        if ext == '.xlsx' and file_format == 'zip':
            engine = 'openpyxl'
        elif ext == '.xls' and file_format == 'xls':
            engine = 'xlrd'
        else:
            raise TypeError('Wrong format for Excel parsing.')

        self.sheet_names = pd.ExcelFile(excel_fpath, engine=engine).sheet_names

        # read only specified sheets
        self.sheet_indexes = sheet_indexes

        if not sheet_indexes:
            self.sheet_indexes = [i for i, _ in enumerate(self.sheet_names)]

        # skip specified number of rows from top
        self.skip_rows = skip_rows

        if not skip_rows:
            self.skip_rows = [0 for i in self.sheet_names]
        else:
            self.skip_rows = [skip_rows for i in self.sheet_names]

        # use X:X like range
        self.use_cols = use_cols

    @property
    def percent_done(self):
        total = len(self.sheet_names)
        return floor((self.parsed_sheets * 100)/total)

    @property
    def status(self):
        s = f'Total: {len(self.sheet_names)}'
        s += f'Parsed: {self.parsed_rows} rows, {self.parsed_sheets} sheets.'
        return

    def __iter__(self):

        for sh_i in self.sheet_indexes:
            df = pd.read_excel(self.excel_fpath,
                               sheet_name=self.sheet_names[sh_i],
                               skiprows=self.skip_rows[sh_i],
                               usecols=self.use_cols,
                               index_col=None,
                               dtype=str,
                               header=None
                               )

            # convert Excel's empty cells to empty string
            data = df.replace(np.nan, '', regex=True)
            data.dropna(inplace=True)
            self.parsed_sheets += 1
            self.parsed_rows += len(data.values)
            yield data.values
