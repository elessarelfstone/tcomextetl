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
class DgovDatasets305PerechenGosudarstvennyh1Row:
    spec_rus = field(default='')
    forma_rus = field(default='')
    region_rus = field(default='')
    name_rus = field(default='')
    period_kaz = field(default='')
    region_kaz = field(default='')
    forma_kaz = field(default='')
    adress_kaz = field(default='')
    id = field(default='')
    name_kaz = field(default='')
    spec_kaz = field(default='')
    adress_rus = field(default='')
    period_rus = field(default='')


@define
class DgovDatasets306PerechenGosudarstvennyhRow:
    spec_rus = field(default='')
    forma_rus = field(default='')
    region_rus = field(default='')
    name_rus = field(default='')
    period_kaz = field(default='')
    region_kaz = field(default='')
    forma_kaz = field(default='')
    adress_kaz = field(default='')
    id = field(default='')
    name_kaz = field(default='')
    spec_kaz = field(default='')
    adress_rus = field(default='')
    period_rus = field(default='')


@define
class DgovDatasets307PerechenGosudarstvennyh1Row:
    spec_rus = field(default='')
    forma_rus = field(default='')
    region_rus = field(default='')
    name_rus = field(default='')
    period_kaz = field(default='')
    region_kaz = field(default='')
    forma_kaz = field(default='')
    adress_kaz = field(default='')
    id = field(default='')
    name_kaz = field(default='')
    spec_kaz = field(default='')
    adress_rus = field(default='')
    period_rus = field(default='')


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


@define
class DgovDatasets375PerechenGosudarstvennyh3Row:
    spec_rus = field(default='')
    forma_rus = field(default='')
    region_rus = field(default='')
    svob_mest = field(default='')
    index = field(default='')
    name_rus = field(default='')
    period_kaz = field(default='')
    region_kaz = field(default='')
    forma_kaz = field(default='')
    adress_kaz = field(default='')
    id = field(default='')
    name_kaz = field(default='')
    spec_kaz = field(default='')
    adress_rus = field(default='')
    kol_mest = field(default='')
    period_rus = field(default='')


@define
class DgovDatasets305PerechenGosudarstvennyhRow:
    id = field(default='')
    mail = field(default='')
    adress_kz = field(default='')
    operating = field(default='')
    name_ru = field(default='')
    internet = field(default='')
    fio = field(default='')
    name_kz = field(default='')
    contacts = field(default='')
    adress_ru = field(default='')


@define
class DgovDatasetsMemlekettikAuruhanalarTizbesRow:
    field_3 = field(default='')
    field_2 = field(default='')
    field_1 = field(default='')
    field_7 = field(default='')
    field_6 = field(default='')
    field_5 = field(default='')
    field_4 = field(default='')


@define
class DgovDatasetsMugedektigiBarAdamdargaArnaRow:
    field_3 = field(default='')
    field_2 = field(default='')
    field_1 = field(default='')


@define
class DgovDatasetsAtaAnasynynKamkorlygynsyzKaRow:
    field_3 = field(default='')
    field_2 = field(default='')
    field_1 = field(default='')


@define
class DgovDatasetsMemlekettikAuruhanalarTizbes1Row:
    field_3 = field(default='')
    field_2 = field(default='')
    field_1 = field(default='')


@define
class DgovDatasetsPerechenGosudarstvennyhRodiRow:
    id = field(default='')
    rezhim = field(default='')
    adres = field(default='')
    naimenovan = field(default='')
    uslugi = field(default='')
    telefon = field(default='')
    pochta = field(default='')


@define
class DgovDatasetsPerechenGosudarstvennyhDispRow:
    id = field(default='')
    rezhim = field(default='')
    adres = field(default='')
    naimenovan = field(default='')
    uslugi = field(default='')
    telefon = field(default='')
    pochta = field(default='')


@define
class DgovDatasetsPerechenGosudarstvennyhBolRow:
    id = field(default='')
    rezhim = field(default='')
    adres = field(default='')
    naimenovan = field(default='')
    uslugi = field(default='')
    telefon = field(default='')
    pochta = field(default='')


@define
class DgovDatasets304PerechenGosudarstvennyhRow:
    mail = field(default='')
    adress_kz = field(default='')
    operating = field(default='')
    name_ru = field(default='')
    official = field(default='')
    fio = field(default='')
    name_kz = field(default='')
    contacts = field(default='')
    adress_ru = field(default='')


@define
class DgovDatasets307PerechenGosudarstvennyhRow:
    mail = field(default='')
    adress_kz = field(default='')
    operating = field(default='')
    name_ru = field(default='')
    fio = field(default='')
    name_kz = field(default='')
    contacts = field(default='')
    adress_ru = field(default='')


@define
class DgovDatasetsGrdVkoRow:
    phone_number = field(default='')
    official_internet_resource = field(default='')
    geoposition = field(default='')
    contact_numbers = field(default='')
    full_name_director = field(default='')
    idrow = field(default='')
    travel_bus_routes = field(default='')
    working_hours_kz = field(default='')
    days_of_reception = field(default='')
    location_kz = field(default='')
    types_services_kz = field(default='')
    equipment_kz = field(default='')
    location_ru = field(default='')
    equipment_ru = field(default='')
    name_kz = field(default='')
    working_hours_ru = field(default='')
    id = field(default='')
    types_services_ru = field(default='')
    date_of_dispatch = field(default='')
    name_ru = field(default='')
    registry = field(default='')
    number_of_beds = field(default='')
    email_address = field(default='')


@define
class DgovDatasetsPgbVkoRow:
    travel_by_bus = field(default='')
    phone = field(default='')
    official_internet_resource = field(default='')
    types_of_services_ru = field(default='')
    address_kz = field(default='')
    full_name_of_the_director = field(default='')
    types_of_services_kz = field(default='')
    geoposition = field(default='')
    idrow = field(default='')
    working_hours_kz = field(default='')
    days_of_reception = field(default='')
    address_ru = field(default='')
    equipment_kz = field(default='')
    equipment_ru = field(default='')
    name_kz = field(default='')
    working_hours_ru = field(default='')
    id = field(default='')
    date_of_dispatch = field(default='')
    name_ru = field(default='')
    registry = field(default='')
    number_of_beds = field(default='')
    phone_number_of_the_director = field(default='')
    email_address = field(default='')


@define
class DgovDatasetsPsioVkoRow:
    district_ru = field(default='')
    phone = field(default='')
    address_kz = field(default='')
    full_name_of_the_director = field(default='')
    direction_of_activity_kz = field(default='')
    geoposition = field(default='')
    idrow = field(default='')
    working_hours_kz = field(default='')
    address_ru = field(default='')
    direction_of_activity_ru = field(default='')
    name_kz = field(default='')
    district_kz = field(default='')
    working_hours_ru = field(default='')
    id = field(default='')
    number_of_students = field(default='')
    date_of_dispatch = field(default='')
    name_ru = field(default='')
    email_address = field(default='')