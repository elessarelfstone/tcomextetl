from attrs import define, field


@define
class DgovAddrRegDAtsTypes:
    actual = field(default='')
    code = field(default='')
    value_ru = field(default='')
    short_value_kz = field(default='')
    id = field(default='')
    short_value_ru = field(default='')
    value_kz = field(default='')


@define
class DgovAddrRegDBuildingsPointers:
    actual = field(default='')
    code = field(default='')
    value_ru = field(default='')
    short_value_kz = field(default='')
    id = field(default='')
    short_value_ru = field(default='')
    value_kz = field(default='')


@define
class DgovAddrRegDGeonimsTypes:
    actual = field(default='')
    code = field(default='')
    value_ru = field(default='')
    short_value_kz = field(default='')
    id = field(default='')
    short_value_ru = field(default='')
    value_kz = field(default='')


@define
class DgovAddrRegDRoomsTypes:
    actual = field(default='')
    code = field(default='')
    value_ru = field(default='')
    short_value_kz = field(default='')
    id = field(default='')
    short_value_ru = field(default='')
    value_kz = field(default='')


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


@define
class DgovAddrRegSAtsRow:
    id = field(default='')
    rco = field(default='')
    name_rus = field(default='')
    name_kaz = field(default='')
    full_path_kaz = field(default='')
    full_path_rus = field(default='')
    d_ats_type_id = field(default='')
    d_ats_type_code = field(default='')
    cato = field(default='')
    actual = field(default='')
    parent_id = field(default='')
    modified = field(default='')


@define
class DgovAddrRegSGeonimsRow:
    id = field(default='')
    full_path_rus = field(default='')
    rco = field(default='')
    name_kaz = field(default='')
    full_path_kaz = field(default='')
    cato = field(default='')
    s_ats_id = field(default='')
    name_rus = field(default='')
    actual = field(default='')
    d_geonims_type_id = field(default='')
    parent_id = field(default='')
    modified = field(default='')
    

@define
class DgovAddrRegSGroundsRow:
    id = field(default='')
    s_geonim_id = field(default='')
    full_path_rus = field(default='')
    full_path_kaz = field(default='')
    cadastre_number = field(default='')
    s_ats_id = field(default='')
    actual = field(default='')
    number = field(default='')
    rca = field(default='')
    modified = field(default='')


@define
class DgovAddrRegSBuildingsRow:
    s_geonim_id = field(default='')
    d_buildings_pointer_id = field(default='')
    number = field(default='')
    modified = field(default='')
    full_path_rus = field(default='')
    id = field(default='')
    full_path_kaz = field(default='')
    distance = field(default='')
    this_is = field(default='')
    s_ats_id = field(default='')
    actual = field(default='')
    d_buildings_pointer_code = field(default='')
    parent_rca = field(default='')
    s_ground_id = field(default='')
    rca = field(default='')
    parent_id = field(default='')





