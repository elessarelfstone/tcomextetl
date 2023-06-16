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
    order_no = field(default='')


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

    for i, r in enumerate(rows, start=1):
        r.order_no = i
