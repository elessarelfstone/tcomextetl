from attrs import define, field


@define
class BankruptRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    court_decision = field(default='')
    court_decision_date = field(default='')


@define
class InactiveRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    owner_no = field(default='')
    order_date = field(default='')


@define
class InvregistrationRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    court_decision_no = field(default='')
    court_decision_date = field(default='')


@define
class JwaddressRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    inspection_act_no = field(default='')
    inspection_date = field(default='')


@define
class PseudocompanyRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    court_decision = field(default='')
    illegal_activity_start_date = field(default='')


@define
class TaxArrears150Row:
    num = field(default='')
    region = field(default='')
    office_of_tax_enforcement = field(default='')
    ote_id = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization_ru = field(default='')
    taxpayer_organization_kz = field(default='')
    last_name_kz = field(default='')
    first_name_kz = field(default='')
    middle_name_kz = field(default='')
    last_name_ru = field(default='')
    first_name_ru = field(default='')
    middle_name_ru = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    owner_name_kz = field(default='')
    owner_name_ru = field(default='')
    economic_sector = field(default='')
    total_due = field(default='')
    sub_total_main = field(default='')
    sub_total_late_fee = field(default='')
    sub_total_fine = field(default='')


@define
class TaxViolatorsRow:
    num = field(default='')
    bin = field(default='')
    rnn = field(default='')
    taxpayer_organization = field(default='')
    taxpayer_name = field(default='')
    owner_name = field(default='')
    owner_iin = field(default='')
    owner_rnn = field(default='')
    inspection_act_no = field(default='')
    inspection_date = field(default='')


@define
class TaxPaymentsRow:
    bin = field(default='')
    taxorgcode = field(default='')
    nametaxru = field(default='')
    nametaxkz = field(default='')
    kbk = field(default='')
    kbknameru = field(default='')
    kbknamekz = field(default='')
    paynum = field( default='')
    paytype = field(default='')
    entrytype = field(default='')
    receiptdate = field(default='')
    writeoffdate = field(default='')
    summa = field(default='')
