import os

import attr

CSV_SEP = ';'
CSV_SEP_REPLACEMENT = ' '


def clean(value: str):

    # remove separator
    v = str(value).replace(CSV_SEP, CSV_SEP_REPLACEMENT)

    # remove trailing newline
    v = v.strip().replace('\n', '').replace('\r', '')

    # remove double quotes
    v = v.replace('"', "'")

    return v


def save_csvrows(fpath: str, recs, sep=None, quoter=None):
    """ Save list of tuples as csv rows to file """

    _sep = CSV_SEP
    if sep:
        _sep = sep

    _q = ''
    if quoter:
        _q = quoter

    with open(fpath, 'a+', encoding="utf-8") as f:
        for rec in recs:
            # clean
            _rec = [clean(v) for v in rec]
            # quoting
            _rec = [f'{_q}{v}{_q}' for v in _rec]
            row = _sep.join(_rec)
            f.write(row + '\n')

    return len(recs)


def dict_to_csvrow(p_dict, struct):
    """ Convert given dict into tuple using
    given structure(attr class)."""

    # cast each keys's name of dict to lower case
    src_dict = {k.lower(): v for k, v in p_dict.items() if k.lower()}

    # get fields of structure
    keys = [a.name for a in attr.fields(struct)]

    d = {}

    # build new dict with fields specified in struct
    for k in keys:
        if k in src_dict.keys():
            d[k] = src_dict[k]

    # wrap in struct
    attr_obj = struct(**d)

    return attr.astuple(attr_obj)


