from attrs import define, field


@define
class KatoRow:
    te = field(default='')
    ab = field(default='')
    cd = field(default='')
    ef = field(default='')
    hij = field(default='')
    k = field(default='')
    name_kaz = field(default='')
    name_rus = field(default='')
    nn = field(default='')


@define
class OkedRow:
    code = field(default='')
    namekz = field(default='')
    nameru = field(default='')
    lv0 = field(default='')
    lv1 = field(default='')
    lv2 = field(default='')
    lv3 = field(default='')


@define
class MkeisRow:
    code = field(default='')
    namekz = field(default='')
    nameru = field(default='')


@define
class KurkRow:
    code = field(default='')
    namekz = field(default='')
    nameru = field(default='')


@define
class KpvedRow:
    code = field(default='')
    namekz = field(default='')
    nameru = field(default='')


@define
class CompanieRow:
    bin = field(default='')
    full_name_kz = field(default='')
    full_name_ru = field(default='')
    registration_date = field(default='')
    oked_1 = field(default='')
    activity_kz = field(default='')
    activity_ru = field(default='')
    oked_2 = field(default='')
    krp = field(default='')
    krp_name_kz = field(default='')
    krp_name_ru = field(default='')
    kato = field(default='')
    settlement_kz = field(default='')
    settlement_ru = field(default='')
    legal_address = field(default='')
    head_fio = field(default='')


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


