import attr

CSV_DELIMITER = ';'
CSV_DELIMITER_REPLACEMENT = ' '
CSV_QUOTECHAR = '"'


def save_csvrows(fpath: str, rows, delimiter=None, quotechar=CSV_QUOTECHAR):
    """ Save list of tuples as csv rows to file """

    def prepare(value):
        val = value

        if type(value) == str:
            # clean new-line and carriage returns
            val = ''.join(filter(lambda ch: ch not in "\n\r", val))
            # quote if delimiter found
            if d in val:
                val = f'{quotechar}{val}{quotechar}'

        return val

    d = CSV_DELIMITER

    if delimiter:
        d = delimiter

    with open(fpath, 'a+', encoding="utf-8") as f:
        for row in rows:
            _row = []
            for v in row:
                _row.append(prepare(v))
            csv_row = d.join(f'{value}' for value in _row)
            f.write(csv_row + '\n')

    return len(rows)


def dict_to_csvrow(p_dict, struct):
    """ Convert given dict into tuple using
    given structure(attr class). """

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
