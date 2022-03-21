import json

from openpyxl import Workbook

from tcomextetl.common.utils import read_file


def save_test_data_in_excel(excel_fpath):
    wb = Workbook()
    ws_active = wb.active
    sheet_num = 1
    ws_active.title = str(sheet_num)
    test_data = json.loads(read_file('excel_data.json'))

    for sh in test_data:
        for row in sh:
            ws_active.append(tuple(row.values()))
        sheet_num += 1
        if sheet_num <= len(test_data):
            ws_active = wb.create_sheet(title=str(sheet_num))

    wb.save(filename=excel_fpath)


save_test_data_in_excel("C:\\Users\\elessar\\excel_test.xlsx")

