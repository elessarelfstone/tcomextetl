import attr


@attr.s
class BankruptRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    court_decision = attr.ib(default='')
    court_decision_date = attr.ib(default='')


@attr.s
class InactiveRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    owner_no = attr.ib(default='')
    order_date = attr.ib(default='')


@attr.s
class InvregistrationRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    court_decision_no = attr.ib(default='')
    court_decision_date = attr.ib(default='')


@attr.s
class JwaddressRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    inspection_act_no = attr.ib(default='')
    inspection_date = attr.ib(default='')


@attr.s
class PseudocompanyRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    court_decision = attr.ib(default='')
    illegal_activity_start_date = attr.ib(default='')


@attr.s
class TaxArrears150Row:
    num = attr.ib(default='')
    region = attr.ib(default='')
    office_of_tax_enforcement = attr.ib(default='')
    ote_id = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization_ru = attr.ib(default='')
    taxpayer_organization_kz = attr.ib(default='')
    last_name_kz = attr.ib(default='')
    first_name_kz = attr.ib(default='')
    middle_name_kz = attr.ib(default='')
    last_name_ru = attr.ib(default='')
    first_name_ru = attr.ib(default='')
    middle_name_ru = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    owner_name_kz = attr.ib(default='')
    owner_name_ru = attr.ib(default='')
    economic_sector = attr.ib(default='')
    total_due = attr.ib(default='')
    sub_total_main = attr.ib(default='')
    sub_total_late_fee = attr.ib(default='')
    sub_total_fine = attr.ib(default='')


@attr.s
class TaxViolatorsRow:
    num = attr.ib(default='')
    bin = attr.ib(default='')
    rnn = attr.ib(default='')
    taxpayer_organization = attr.ib(default='')
    taxpayer_name = attr.ib(default='')
    owner_name = attr.ib(default='')
    owner_iin = attr.ib(default='')
    owner_rnn = attr.ib(default='')
    inspection_act_no = attr.ib(default='')
    inspection_date = attr.ib(default='')
