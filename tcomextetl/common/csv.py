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

            # clean slashes
            val = val.strip("/").replace('\\', '')

            if CSV_QUOTECHAR in val:
                val = val.replace(CSV_QUOTECHAR, "'").strip(CSV_QUOTECHAR)

            # quote if delimiter found
            if CSV_DELIMITER in val:
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


def dict_to_row(p_dict, data_class):
    """ Convert given dict into tuple using
    given data class(attr class). """

    # cast each keys's name of dict to lower case
    _dict = {k.lower(): v for k, v in p_dict.items() if k.lower()}

    # get fields of structure
    keys = [a.name for a in attr.fields(data_class)]

    d = {}

    # build new dict with fields specified in data class
    for k in keys:
        if k in _dict.keys():
            d[k] = _dict[k]

    # wrap in data class
    attr_instance = data_class(**d)

    return attr.astuple(attr_instance)
