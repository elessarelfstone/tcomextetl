from attrs import define, field


@define
class DgovDatasetsPrivateSchoolsRow:
    education_ = field(default='')
    area_id = field(default='')
    sdu_load_i = field(default='')
    region_id = field(default='')
    district_n = field(default='')
    district_i = field(default='')
    long = field(default='')
    establish_ = field(default='')
    id = field(default='')
    student_co = field(default='')
    address = field(default='')
    region_nam = field(default='')
    geo_coordi = field(default='')
    area_name = field(default='')
    lat = field(default='')


@define
class DgovDatasetsMedicalOrgRow:
    id = field(default='')
    area_id = field(default='')
    sdu_load_i = field(default='')
    address_li = field(default='')
    status = field(default='')
    area_name = field(default='')
