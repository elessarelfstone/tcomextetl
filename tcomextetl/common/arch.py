import os
import fnmatch
from shutil import move

from zipfile import ZipFile
from rarfile import RarFile

from tcomextetl.common.utils import identify_file_format
from tcomextetl.common.exceptions import ExternalSourceError


def extract_by_wildcard(arch_fpath: str, wildcard: str = '*.xlsx', paths=None):

    """ Extract files from archive. Supports only zip and rar formats. """

    frmt = identify_file_format(arch_fpath)

    # detect archive format
    if not frmt:
        raise ExternalSourceError("Not supported format")
    else:
        if frmt == 'rar':
            arch_obj = RarFile(arch_fpath)
        else:
            arch_obj = ZipFile(arch_fpath)

    # directory where to extract
    _dir = os.path.abspath(os.path.dirname(arch_fpath))

    # filter by wildcard
    files_to_extract = fnmatch.filter(arch_obj.namelist(), wildcard)

    # slice
    if paths:
        files_to_extract = files_to_extract[:len(paths)]

    extracted_files_list = []

    for i, f in enumerate(files_to_extract):
        arch_obj.extract(f, _dir)
        src = os.path.join(_dir, f).replace('/', os.sep)
        dest = paths[i]
        move(src, dest)
        extracted_files_list.append(dest)

    return extracted_files_list

