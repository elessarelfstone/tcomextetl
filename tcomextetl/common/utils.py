import csv
from pathlib import Path
from collections import namedtuple

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from settings import PARAMS_CONFIG_PATH

FILE_FORMATS = [
    {"extension": "zip", "mime": "application/zip", "offset": 0, "signature": "50 4B 03 04"},
    {"extension": "tar", "mime": "application/x-tar", "offset": 257, "signature": "75 73 74 61 72"},
    {"extension": "gzip", "mime": "application/gzip", "offset": 0, "signature": "1F 8B 08"},
    {"extension": "7z", "mime": "application/x-7z-compressed", "offset": 0, "signature": "37 7A BC AF 27 1C"},
    {"extension": "rar", "mime": "application/x-rar-compressed", "offset": 0, "signature": "52 61 72 21 1A 07 01 00"},
    {"extension": "rar", "mime": "application/rar", "offset": 0, "signature": "52 61 72 21 1A 07 00"},
    {"extension": "xlsx", "mime": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "offset": 0,
     "signature": "50 4B 03 04 14 00 06 00"},
    {"extension": "xls", "mime": "application/vnd.ms-excel", "offset": 0, "signature": "D0 CF 11 E0 A1 B1 1A E1"}
]

# bytes pretty-printing
UNITS_MAPPING = [
    (1 << 50, ' PB'),
    (1 << 40, ' TB'),
    (1 << 30, ' GB'),
    (1 << 20, ' MB'),
    (1 << 10, ' KB'),
    (1, (' byte', ' bytes')),
]

# handy working with formats
Formats = namedtuple('Formats', ['extension', 'mime', 'offset', 'signature'])


def read_file(fpath: str) -> str:
    """ Return all rows of file as string """
    with open(fpath, 'r', encoding="utf8") as f:
        data = f.read().rstrip('\r\n')

    return data


def read_lines(fpath):
    """ Return rows of file as list """
    with open(fpath, "r", encoding="utf-8") as f:
        lines = [b.rstrip() for b in f.readlines()]

    return lines


def append_file(fpath, data):
    with open(fpath, 'a+', encoding="utf8") as f:
        f.write(data + '\n')


def rewrite_file(fpath, data):
    with open(fpath, 'w', encoding="utf8") as f:
        f.write(data + '\n')


def pretty_size(p_bytes):
    """ Get human-readable file sizes. """

    factor, suffix = None, None

    for factor, suffix in UNITS_MAPPING:
        if p_bytes >= factor:
            break

    amount = int(p_bytes / factor)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def file_formats():

    # wrap in Formats struct
    _formats = []
    for f in FILE_FORMATS:
        _formats.append(Formats(**f))

    return _formats


def identify_file_format(fpath: str) -> str:
    """ Read signature of file and return format if it's supported """

    _formats = file_formats()

    # read first N bytes
    with open(fpath, "rb") as file:
        # 300 bytes are enough
        header = file.read(500)

    # convert to hex
    stream = " ".join(['{:02X}'.format(byte) for byte in header])

    for frmt in _formats:
        # if there is offset
        offset = frmt.offset * 2 + frmt.offset
        if frmt.signature == stream[offset:len(frmt.signature) + offset]:
            return frmt.extension

    return None


def build_fpath(directory: str, name: str, ext: str, suff: str = None):
    d = Path(directory)
    name = '_'.join([name, suff]) if suff else name
    return d.joinpath(name).with_suffix(ext)


def get_yaml_task_config(fpath, section):
    with open(fpath) as c:
        config = load(c, Loader=Loader)

    return config[section]


def flatten_data(d):
    """ """

    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(d)

    return out

# class CsvValuesHandler:
#
#     def __init__(self, source_fpath, parsed_fpath, sep=';', columns=None):
#         source_vals = []
#         with open(source_fpath) as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=sep)
#             for row in csv_reader:
#                 if columns:
#                     for c in columns:
