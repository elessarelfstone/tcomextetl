from attrs import define, field


@define
class DgovAddrRegSPbRow:
    id = field(default='')
    d_room_type_id = field(default='')
    full_path_rus = field(default='')
    full_path_kaz = field(default='')
    actual = field(default='')
    s_building_id = field(default='')
    number = field(default='')
    rca = field(default='')
    modified = field(default='')
