Унифицированные сервисы с данными по государственным закупкам
-------------------------------------------------------------


Реестр участников государственных закупок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: goszakup_companies

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-uchastnikov-reestr-uchastnikov-polnyi-spisok

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/subject.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupCompanies



Реестр договоров
~~~~~~~~~~~~~~~~


Код в проекте: goszakup_contracts

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-dogovorov-polnaia-informatsiia-po-dogovoram

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/contract.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupContracts


Реестр лотов
~~~~~~~~~~~~


Код в проекте: goszakup_lots

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-lotov-reestr-lotov

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/lots.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupLots


Реестр объявлений
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_trd_buys

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#ob-iavleniia-o-gos-zakupkakh-poluchenie-polnogo-spiska-ob-iavlenii

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/trdbuy.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupTrdBuys


Реестр годовых планов
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_plan_points

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-godovykh-planov-reestr-punktov-plana

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/plnpoint.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupPlanPoints


Места поставки пункта плана
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_plans_kato

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-godovykh-planov-reestr-mest-postavki

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/plnpointskato.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupPlansKato


Места поставки пункта плана
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_plans_kato

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-godovykh-planov-reestr-mest-postavki

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/plnpointskato.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupPlansKato


Предметы договора
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_contract_units

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-dogovorov-predmety-dogovora

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/contractunits.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupContractUnits


Предметы договора
~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_contract_units

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-dogovorov-predmety-dogovora

Ссылка на документацию GraphQL: https://ows.goszakup.gov.kz/help/v3/schema/contractunits.doc.html

Класс-структура:

..  code-block:: python

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

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupContractUnits


Реестр недобросовестных поставщиков
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Код в проекте: goszakup_untrusted

Формат: api, json

Ссылка на документацию REST: https://goszakup.gov.kz/ru/developer/ows_v3#reestr-nedobrosovestnykh-postavshchikov-reestr-nedobrosovestnykh-postavshchikov

Класс-структура:

..  code-block:: python

   class GoszakupUntrustedSupplierRow:
        pid = field(default='')
        supplier_biin = field(default='')
        supplier_innunp = field(default='')
        supplier_name_ru = field(default='')
        supplier_name_kz = field(default='')
        kato_list = field(default='')
        index_date = field(default='')
        system_id = field(default='')

Запуск из контейнера:

..  code-block:: bash

    GOSZAKUP_TOKEN="<GOSZAKUP_TOKEN>" docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupUntrusted
