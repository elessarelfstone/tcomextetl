from attrs import define, field


@define
class DgovDatasetsPrivateSchoolRow:
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


@define
class DgovDatasetsStateSchoolRow:
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
class DgovDatasetsHigherEducationOrgRow:
    education_ = field(default='')
    area_id = field(default='')
    sdu_load_i = field(default='')
    number_stu = field(default='')
    region_id = field(default='')
    district_n = field(default='')
    district_i = field(default='')
    graduates = field(default='')
    long = field(default='')
    establish_ = field(default='')
    id = field(default='')
    address = field(default='')
    region_nam = field(default='')
    geo_coordi = field(default='')
    area_name = field(default='')
    lat = field(default='')


@define
class DgovDatasetsRosogrzMpRow:
    id = field(default='')
    school_number = field(default='')
    school_type = field(default='')
    school_address = field(default='')
    school_name = field(default='')
    name_region = field(default='')


@define
class DgovDatasetsKarzhyUimdarynynIriKaRow:
    id = field(default='')
    namekukz = field(default='')
    nameorgkz = field(default='')
    nameorgru = field(default='')
    namekuru = field(default='')


@define
class DgovDatasetsMemlekettikBalabakshalarTuraRow:
    id = field(default='')
    vozrast_gr = field(default='')
    adress_kz = field(default='')
    kontakty = field(default='')
    rejim_rab = field(default='')
    naim_kz = field(default='')
    naim_ru = field(default='')
    fio_rukov = field(default='')
    adress_ru = field(default='')


@define
class DgovDatasetsPerechenGosudarstvennyhRow:
    id = field(default='')
    region_rus = field(default='')
    namerus = field(default='')
    addresska = field(default='')
    region_kaz = field(default='')
    period = field(default='')
    telephone = field(default='')
    addressru = field(default='')
    namekaz = field(default='')


@define
class DgovDatasetsOstvkoRow:
    region = field(default='')
    phone = field(default='')
    website = field(default='')
    servicesru = field(default='')
    namekz = field(default='')
    nameru = field(default='')
    addressru = field(default='')
    addresskz = field(default='')
    scheduleru = field(default='')
    id = field(default='')
    email = field(default='')
    geoposit = field(default='')
    schedulekz = field(default='')
    head = field(default='')
    serviceskz = field(default='')


@define
class DgovDatasetsOpendataApiUriRow:
    id = field(default='')
    region_ru = field(default='')
    fio_ru = field(default='')
    kontakt_ru = field(default='')
    fio_kz = field(default='')
    region_kz = field(default='')
    kontakt_kz = field(default='')


@define
class DgovDatasetsPerechenGosudarstvennyhOrgaRow:
    pocta = field(default='')
    id = field(default='')
    naimenkz = field(default='')
    rezhim = field(default='')
    adres = field(default='')
    telefon = field(default='')
    naimenru = field(default='')
    fio = field(default='')


@define
class DgovDatasetsMu1021Row:
    id = field(default='')
    kolvosmal = field(default='')
    kolvomedium = field(default='')
    oblastru = field(default='')
    kolvomajor = field(default='')
    oblastkz = field(default='')


@define
class DgovDatasetsMu101Row:
    id = field(default='')
    kolvo = field(default='')
    oblastru = field(default='')
    oblastkz = field(default='')


@define
class DgovDatasetsMu100Row:
    id = field(default='')
    kolvo = field(default='')
    oblastru = field(default='')
    oblastkz = field(default='')
