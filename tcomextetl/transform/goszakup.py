from attrs import define, field


@define
class GoszakupCompanyRow:
    pid = field(default='')
    bin = field(default='')
    iin = field(default='')
    inn = field(default='')
    unp = field(default='')
    regdate = field(default='')
    crdate = field(default='')
    number_reg = field(default='')
    series = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    email = field(default='')
    phone = field(default='')
    website = field(default='')
    last_update_date = field(default='')
    country_code = field(default='')
    qvazi = field(default='')
    customer = field(default='')
    organizer = field(default='')
    mark_national_company = field(default='')
    ref_kopf_code = field(default='')
    mark_assoc_with_disab = field(default='')
    year = field(default='')
    mark_resident = field(default='')
    system_id = field(default='')
    supplier = field(default='')
    krp_code = field(default='')
    oked_list = field(default='')
    kse_code = field(default='')
    mark_world_company = field(default='')
    mark_state_monopoly = field(default='')
    mark_natural_monopoly = field(default='')
    mark_patronymic_producer = field(default='')
    mark_patronymic_supplyer = field(default='')
    mark_small_employer = field(default='')
    type_supplier = field(default='')
    is_single_org = field(default='')
    index_date = field(default='')


@define
class GoszakupContractRow:
    id = field(default='')
    parent_id = field(default='')
    root_id = field(default='')
    trd_buy_id = field(default='')
    trd_buy_number_anno = field(default='')
    trd_buy_name_ru = field(default='')
    trd_buy_name_kz = field(default='')
    ref_contract_status_id = field(default='')
    deleted = field(default='')
    crdate = field(default='')
    last_update_date = field(default='')
    supplier_id = field(default='')
    supplier_biin = field(default='')
    supplier_bik = field(default='')
    supplier_iik = field(default='')
    supplier_bank_name_kz = field(default='')
    supplier_bank_name_ru = field(default='')
    supplier_legal_address = field(default='')
    supplier_bill_id = field(default='')
    contract_number = field(default='')
    sign_reason_doc_name = field(default='')
    sign_reason_doc_date = field(default='')
    trd_buy_itogi_date_public = field(default='')
    customer_id = field(default='')
    customer_bin = field(default='')
    customer_bik = field(default='')
    customer_iik = field(default='')
    customer_bill_id = field(default='')
    customer_bank_name_kz = field(default='')
    customer_bank_name_ru = field(default='')
    customer_legal_address = field(default='')
    contract_number_sys = field(default='')
    payments_terms_ru = field(default='')
    payments_terms_kz = field(default='')
    ref_subject_type_id = field(default='')
    ref_subject_types_id = field(default='')
    is_gu = field(default='') # integer
    fin_year = field(default='') # integer
    ref_contract_agr_form_id = field(default='')
    ref_contract_year_type_id = field(default='')
    ref_finsource_id = field(default='')
    ref_currency_code = field(default='')
    exchange_rate = field(default='')
    contract_sum = field(default='')
    contract_sum_wnds = field(default='')
    sign_date = field(default='')
    ec_end_date = field(default='')
    plan_exec_date = field(default='')
    fakt_exec_date = field(default='')
    fakt_sum = field(default='')
    fakt_sum_wnds = field(default='')
    contract_end_date = field(default='')
    ref_contract_cancel_id = field(default='')
    ref_contract_type_id = field(default='')
    description_kz = field(default='')
    description_ru = field(default='')
    fakt_trade_methods_id = field(default='')
    ec_customer_approve = field(default='')
    ec_supplier_approve = field(default='')
    contract_ms = field(default='')
    treasure_req_num = field(default='')
    treasure_req_date = field(default='')
    treasure_not_num = field(default='')
    treasure_not_date = field(default='')
    system_id = field(default='')
    index_date = field(default='')


@define
class GoszakupUntrustedSupplierRow:
    pid = field(default='')
    supplier_biin = field(default='')
    supplier_innunp = field(default='')
    supplier_name_ru = field(default='')
    supplier_name_kz = field(default='')
    kato_list = field(default='')
    index_date = field(default='')
    system_id = field(default='')


@define
class GoszakupContractTypeRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')


@define
class GoszakupContractStatusRow:
    id = field(default='')
    code = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')


@define
class GoszakupTenderMethodRow:
    code = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    is_active = field(default='')
    type = field(default='')
    symbol_code = field(default='')
    f1 = field(default='')
    ord = field(default='')
    f2 = field(default='')
    id = field(default='')


@define
class GoszakupLotsStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupBuyStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupLotsRow:
    id = field(default='')
    lot_number = field(default='')
    ref_lot_status_id = field(default='')
    last_update_date = field(default='')
    union_lots = field(default='')
    count = field(default='')
    amount = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    description_ru = field(default='')
    description_kz = field(default='')
    customer_id = field(default='')
    customer_bin = field(default='')
    trd_buy_number_anno = field(default='')
    trd_buy_id = field(default='')
    dumping = field(default='')
    dumping_lot_price = field(default='')
    psd_sign = field(default='')
    consulting_services = field(default='')
    point_list = field(default='')
    singl_org_sign = field(default='')
    is_light_industry = field(default='')
    is_construction_work = field(default='')
    disable_person_id = field(default='')
    customer_name_kz = field(default='')
    customer_name_ru = field(default='')
    ref_trade_methods_id = field(default='')
    index_date = field(default='')
    system_id = field(default='')


@define
class GoszakupTradeBuyRow:
    id = field(default='')
    number_anno = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    total_sum = field(default='')
    count_lots = field(default='')
    ref_trade_methods_id = field(default='')
    ref_subject_type_id = field(default='')
    customer_bin = field(default='')
    customer_pid = field(default='')
    org_bin = field(default='')
    org_pid = field(default='')
    ref_buy_status_id = field(default='')
    start_date = field(default='')
    repeat_start_date = field(default='')
    repeat_end_date = field(default='')
    end_date = field(default='')
    publish_date = field(default='')
    itogi_date_public = field(default='')
    ref_type_trade_id = field(default='')
    disable_person_id = field(default='')
    discus_start_date = field(default='')
    discus_end_date = field(default='')
    id_supplier = field(default='')
    biin_supplier = field(default='')
    parent_id = field(default='')
    singl_org_sign = field(default='')
    is_light_industry = field(default='')
    is_construction_work = field(default='')
    customer_name_kz = field(default='')
    customer_name_ru = field(default='')
    org_name_kz = field(default='')
    org_name_ru = field(default='')
    system_id = field(default='')
    index_date = field(default='')


@define
class GoszakupPlanRow:
    pid = field(default='')
    bin = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    doc_count = field(default='')


@define
class GoszakupPlanPointRow:
    id = field(default='')
    rootrecord_id = field(default='')
    sys_subjects_id = field(default='')
    sys_organizator_id = field(default='')
    subject_biin = field(default='')
    subject_name_ru = field(default='')
    subject_name_kz = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    ref_trade_methods_id = field(default='')
    ref_units_code = field(default='')
    count = field(default='')
    price = field(default='')
    amount = field(default='')
    ref_months_id = field(default='')
    ref_pln_point_status_id = field(default='')
    pln_point_year = field(default='')
    ref_subject_type_id = field(default='')
    ref_enstru_code = field(default='')
    ref_finsource_id = field(default='')
    ref_abp_code = field(default='')
    is_qvazi = field(default='')
    date_create = field(default='')
    timestamp = field(default='')
    ref_point_type_id = field(default='')
    desc_ru = field(default='')
    desc_kz = field(default='')
    extra_desc_kz = field(default='')
    extra_desc_ru = field(default='')
    sum_1 = field(default='')
    sum_2 = field(default='')
    sum_3 = field(default='')
    supply_date_ru = field(default='')
    prepayment = field(default='')
    ref_justification_id = field(default='')
    ref_amendment_agreem_type_id = field(default='')
    ref_amendm_agreem_justif_id = field(default='')
    contract_prev_point_id = field(default='')
    disable_person_id = field(default='')
    transfer_sys_subjects_id = field(default='')
    transfer_type = field(default='')
    ref_budget_type_id = field(default='')
    createdin_act_id = field(default='')
    is_active = field(default='')
    active_act_id = field(default='')
    is_deleted = field(default='')
    system_id = field(default='')
    index_date = field(default='')
    plan_act_id = field(default='')
    plan_act_number = field(default='')
    ref_plan_status_id = field(default='')
    plan_fin_year = field(default='')
    plan_preliminary = field(default='')
    date_approved = field(default='')


@define
class GoszakupPlanKatoRow:
    id = field(default='')
    pln_points_id = field(default='')
    ref_kato_code = field(default='')
    ref_countries_code = field(default='')
    full_delivery_place_name_ru = field(default='')
    full_delivery_place_name_kz = field(default='')
    count = field(default='')
    is_active = field(default='')
    is_deleted = field(default='')
    system_id = field(default='')
    index_date = field(default='')


@define
class GoszakupUntrustedSupplierRow:
    pid = field(default='')
    supplier_biin = field(default='')
    supplier_innunp = field(default='')
    supplier_name_ru = field(default='')
    supplier_name_kz = field(default='')
    kato_list = field(default='')
    index_date = field(default='')
    system_id = field(default='')


@define
class GoszakupContractUnitsRow:
    contract_id = field(default='')
    id = field(default='')
    lot_id = field(default='')
    pln_point_id = field(default='')
    item_price = field(default='')
    item_price_wnds = field(default='')
    quantity = field(default='')
    total_sum = field(default='')
    total_sum_wnds = field(default='')
    fact_sum = field(default='')
    fact_sum_wnds = field(default='')
    ks_proc = field(default='')
    ks_sum = field(default='')
    deleted = field(default='')
    trd_buy_id = field(default='')
    contract_registry_id = field(default='')
    crdate = field(default='')
    exec_fakt_date = field(default='')
    exec_plan_date = field(default='')
    executed = field(default='')
    parent_id = field(default='')
    root_id = field(default='')
    ref_contract_status_id = field(default='')
    cr_deleted = field(default='')
    ref_amendm_agreem_justif_id = field(default='')
    system_id = field(default='')
    index_date = field(default='')


@define
class GoszakupTrdAppOffersRow:
    id = field(default='')
    lot_id = field(default='')
    app_lot_id = field(default='')
    price = field(default='')
    amount = field(default='')
    system_id = field(default='')
    index_date = field(default='')
    app_lot_point_list = field(default='')
    app_lot_status_id = field(default='')
    app_lot_price = field(default='')
    app_lot_amount = field(default='')
    app_lot_discount_value = field(default='')
    app_lot_discount_price = field(default='')
    app_lot_system_id = field(default='')
    app_lot_index_date = field(default='')
    app_id = field(default='')
    app_buy_id = field(default='')
    app_supplier_id = field(default='')
    app_cr_fio = field(default='')
    app_mod_fio = field(default='')
    app_supplier_bin_iin = field(default='')
    app_prot_id = field(default='')
    app_prot_number = field(default='')
    app_date_apply = field(default='')
    app_system_id = field(default='')
    app_index_date = field(default='')


@define
class GoszakupLotsStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupRefTradeMethodsRow:
    code = field(default='')
    name_kz = field(default='')
    name_ru = field(default='')
    is_active = field(default='')
    type = field(default='')
    symbol_code = field(default='')
    f1 = field(default='')
    ord = field(default='')
    f2 = field(default='')
    id = field(default='')


@define
class GoszakupRefPlnPointStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupRefSubjectTypeRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')


@define
class GoszakupRefBuyStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupRefPriceOfferStatusRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')


@define
class GoszakupRefKatoRow:
    ab = field(default='')
    cd = field(default='')
    ef = field(default='')
    hij = field(default='')
    k = field(default='')
    name_kz = field(default='')
    name_ru = field(default='')
    level = field(default='')
    full_name_ru = field(default='')
    full_name_kz = field(default='')
    code = field(default='')
    parent_code = field(default='')

@define
class GoszakupRefJustificationRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    ref_trade_methods_id = field(default='')

@define
class GoszakupRefTypeTradeRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    ref_trade_method_id = field(default='')

@define
class GoszakupRefContractStatusRow:
    id = field(default='')
    code = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')

@define
class GoszakupRefFinSourceRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    nogz = field(default='')
    code = field(default='')

@define
class GoszakupRefFkrbProgramRow:
    id = field(default='')
    prg = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')

@define
class GoszakupRefFkrbSubProgramRow:
    id = field(default='')
    prg = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    code = field(default='')

@define
class GoszakupRefAmendmentAgreemTypeRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')

@define
class GoszakupRefAmendmAgreemJustifRow:
    id = field(default='')
    name_ru = field(default='')
    name_kz = field(default='')
    cname_kz = field(default='')
    cname_ru = field(default='')