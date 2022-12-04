import csv
import os
import tempfile
from contextlib import contextmanager

import pytest
from attrs import define, field

from tcomextetl.common.csv import save_csvrows, dict_to_row, CSV_DELIMITER


test_data = [
        [
            {'id': 1, 'date': '2022-10-30 23:55:45', 'Price': 56.7},
            {'id': 2, 'date': '"2022-11-05 12:35:00"', 'price': 102.3, 'descr': 'This is \r\n broken string', 'extra': 'extra'},
            {'id': 3, 'date': '2022-12-31 23:59:59', 'price': 1533.56, 'descr': 'This is another\r broken string'},
            {'id': 4, 'date': '2022-01-01 01:01:01', 'price': 3.14, 'Descr': 'This is just another \n broken string'},
            {'id': 5, 'Date': '2022-03-22 13:00:00', 'price': 10000000.0, 'descr': 'This is string ; with delimiter'},
            {'id': 6, 'date': '2022-07-08 02:00:00', 'price': 0.34, 'descr': '"This is quoted string" ; with delimiter"'}
        ],
        [
            (1, '2022-10-30 23:55:45', 56.7, 'None'),
            (2, '"2022-11-05 12:35:00"', 102.3, 'This is \r\n broken string'),
            (3, '2022-12-31 23:59:59', 1533.56, 'This is another\r broken string'),
            (4, '2022-01-01 01:01:01', 3.14, 'This is just another \n broken string'),
            (5, '2022-03-22 13:00:00', 10000000.0, 'This is string ; with delimiter'),
            (6, '2022-07-08 02:00:00', 0.34, '"This is quoted string" ; with delimiter"')
        ],
        [
            ('1', '2022-10-30 23:55:45', '56.7', 'None'),
            ('2', '2022-11-05 12:35:00', '102.3', 'This is  broken string'),
            ('3', '2022-12-31 23:59:59', '1533.56', 'This is another broken string'),
            ('4', '2022-01-01 01:01:01', '3.14', 'This is just another  broken string'),
            ('5', '2022-03-22 13:00:00', '10000000.0', 'This is string ; with delimiter'),
            ('6', '2022-07-08 02:00:00', '0.34', "This is quoted string' ; with delimiter")
        ]
    ]


@define
class CsvRowDataClass:
    id = field(default='')
    date = field(default='')
    price = field(default='')
    descr = field(default='None')


@contextmanager
def open_temp(path, mode):
    file = open(path, mode)
    try:
        yield file
    finally:
        file.close()
        os.unlink(path)


@pytest.fixture(params=[test_data[1:]])
def fixture_save_csvrows(request):

    data = request.param
    data.reverse()

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tf:
        tmp_fpath = tf.name

    return tmp_fpath, data.pop(), data.pop()


def test_save_csvrows(fixture_save_csvrows):

    csv_fpath, rows, res_rows = fixture_save_csvrows
    save_csvrows(csv_fpath, rows)

    rows = []
    with open_temp(csv_fpath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=CSV_DELIMITER)
        for row in csv_reader:
            rows.append(tuple(row))

        assert rows == res_rows


@pytest.mark.parametrize("p_dict, row", list(zip(test_data[0], test_data[1])))
def test_dict_to_row(p_dict, row):
    assert dict_to_row(p_dict, CsvRowDataClass) == row
