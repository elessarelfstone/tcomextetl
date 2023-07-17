from attrs import define, field


@define
class CrmsensorChecklistRow:
    id = field(default='')
    name = field(default='')
    creation_date = field(default='')
    client_communication_date = field(default='')
    region = field(default='')
    unit = field(default='')
    external_id = field(default='')
    employee = field(default='')
    inspector = field(default='')
    result = field(default='')
    conclusion = field(default='')
    question_id = field(default='')
    question_text = field(default='')
    response = field(default='')
