from attrs import define, field, fields


@define
class MirapolisRow:
    event_name = field(default='', metadata={'order': 0})
    event_duration = field(default='', metadata={'order': 1})
    start_event = field(default='', metadata={'order': 2})
    end_event = field(default='', metadata={'order': 3})
    start_event_before = field(default='', metadata={'order': 4})
    end_event_before = field(default='', metadata={'order': 5})
    status_before_event = field(default='', metadata={'order': 6})
    last_name = field(default='', metadata={'order': 7})
    first_name = field(default='', metadata={'order': 8})
    middle_name = field(default='', metadata={'order': 9})
    branch = field(default='', metadata={'order': 10})
    parent_organization = field(default='', metadata={'order': 11})
    department = field(default='', metadata={'order': 12})
    position = field(default='', metadata={'order': 13})
    training_academy = field(default='', metadata={'order': 14})
    location = field(default='', metadata={'order': 15})
    event_format = field(default='', metadata={'order': 16})
    training_provider = field(default='', metadata={'order': 17})
    training_type = field(default='', metadata={'order': 18})
    training_center_location = field(default='', metadata={'order': 19})
    code = field(default='', metadata={'order': 20})
    gender = field(default='', metadata={'order': 21})
    employee_id = field(default='', metadata={'order': 22})
    event_creator = field(default='', metadata={'order': 23})

    @classmethod
    def from_raw(cls, raw):

        d = {}
        for f in fields(cls):
            d[f.name] = raw[str(f.metadata['order'])]

        return d


