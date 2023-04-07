Унифицированные сервисы с данными по государственным закупкам
-------------------------------------------------------------


Реестр участников государственных закупок
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: goszakup_companies

Формат: api, json

Ссылка на документацию: https://ows.goszakup.gov.kz/v3/subject/all

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

    docker-compose -f docker-compose.home.yml run --rm job luigi --module goszakup GoszakupCompanies
