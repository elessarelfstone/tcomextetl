import csv
import os
import tempfile
from contextlib import contextmanager
from tcomextetl.common.csv import save_csvrows, CSV_DELIMITER

from tests.fixtures.fixt_data_funcs import fixture_save_csvrows


@contextmanager
def open_temp(path, mode):
    file = open(path, mode)
    try:
        yield file
    finally:
        file.close()
        # os.unlink(path)


def test_save_csvrows(fixture_save_csvrows):
    data = fixture_save_csvrows
    data.reverse()
    in_rows = data.pop()

    with tempfile.NamedTemporaryFile(suffix='.csv', delete=True) as tf:
        tmp_fpath = tf.name

    out_rows = []

    save_csvrows(tmp_fpath, in_rows)

    with open_temp(tmp_fpath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=CSV_DELIMITER)
        for row in csv_reader:
            out_rows.append(tuple(row))

        assert out_rows == data.pop()







