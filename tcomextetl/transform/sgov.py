import attr


@attr.s
class KatoRow:
    te = attr.ib(default='')
    ab = attr.ib(default='')
    cd = attr.ib(default='')
    ef = attr.ib(default='')
    hij = attr.ib(default='')
    k = attr.ib(default='')
    name_kaz = attr.ib(default='')
    name_rus = attr.ib(default='')
    nn = attr.ib(default='')


@attr.s
class OkedRow:
    code = attr.ib(default='')
    namekz = attr.ib(default='')
    nameru = attr.ib(default='')
    lv0 = attr.ib(default='')
    lv1 = attr.ib(default='')
    lv2 = attr.ib(default='')
    lv3 = attr.ib(default='')


@attr.s
class MkeisRow:
    code = attr.ib(default='')
    namekz = attr.ib(default='')
    nameru = attr.ib(default='')


@attr.s
class KurkRow:
    code = attr.ib(default='')
    namekz = attr.ib(default='')
    nameru = attr.ib(default='')


@attr.s
class KpvedRow:
    code = attr.ib(default='')
    namekz = attr.ib(default='')
    nameru = attr.ib(default='')


@attr.s
class CompanieRow:
    bin = attr.ib(default='')
    full_name_kz = attr.ib(default='')
    full_name_ru = attr.ib(default='')
    registration_date = attr.ib(default='')
    oked_1 = attr.ib(default='')
    activity_kz = attr.ib(default='')
    activity_ru = attr.ib(default='')
    oked_2 = attr.ib(default='')
    krp = attr.ib(default='')
    krp_name_kz = attr.ib(default='')
    krp_name_ru = attr.ib(default='')
    kato = attr.ib(default='')
    settlement_kz = attr.ib(default='')
    settlement_ru = attr.ib(default='')
    legal_address = attr.ib(default='')
    head_fio = attr.ib(default='')


def transform_oked(rows):
    """ Complete each row with levels """
    curr_root = rows[0].code

    for i, r in enumerate(rows):
        if not r.code:
            rows.pop(i)
            continue
        # build new code
        # A, B, C, etc are like roots for a certain code
        if ('.' in r.code) or (r.code.replace('.', '').isdigit()):
            code = f'{curr_root}.{r.code}'
        else:
            code = r.code
            curr_root = r.code

        r.code = r.code.replace('.', '')

        b = code.split('.')
        size = len(b)
        if size == 2:
            r.lv0 = b[0]

        elif size == 3:
            if len(b[2]) == 1:
                r.lv0, r.lv1 = b[0], b[1]
            else:
                r.lv0, r.lv1, r.lv2 = b[0], b[1], f'{b[1]}{b[2][0]}'

        elif size == 4:
            r.lv0, r.lv1, r.lv2, r.lv3 = b[0], b[1], f'{b[1]}{b[2][0]}', f'{b[1]}{b[2]}'


