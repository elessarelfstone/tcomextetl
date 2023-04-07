Реестры сайта Комитета Государственных Доходов Республики Казахстан
-------------------------------------------------


Список налогоплательщиков признанных банкротами
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_bankrupt

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/BANKRUPT/KZ_ALL/fileName/list_BANKRUPT_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class BankruptRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        court_decision = field(default='')
        court_decision_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdBankrupt


Список налогоплательщиков, отсутствующих по юридическому адресу
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_inactive

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/INACTIVE/KZ_ALL/fileName/list_INACTIVE_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class InactiveRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        owner_no = field(default='')
        order_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdInactive


Список налогоплательщиков, регистрация которых признана недействительной
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_invregistration

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/INVALID_REGISTRATION/KZ_ALL/fileName/list_INVALID_REGISTRATION_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class InvregistrationRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        court_decision_no = field(default='')
        court_decision_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdInvregistration


Список налогоплательщиков, отсутствующих по юридическому адресу
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_jwrongaddress

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/WRONG_ADDRESS/KZ_ALL/fileName/list_WRONG_ADDRESS_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class JwaddressRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        inspection_act_no = field(default='')
        inspection_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdWrongAddress



Список налогоплательщиков, признанных лжепредприятиями
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_pseudocompany

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/PSEUDO_COMPANY/KZ_ALL/fileName/list_PSEUDO_COMPANY_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class PseudocompanyRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        court_decision = field(default='')
        illegal_activity_start_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdPseudoCompany


Список налогоплательщиков юридических лиц имеющих налоговую задолженность более 150 МРП
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_taxarrears150

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/TAX_ARREARS_150/KZ_ALL/fileName/list_TAX_ARREARS_150_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class TaxArrears150Row:
        num = field(default='')
        region = field(default='')
        office_of_tax_enforcement = field(default='')
        ote_id = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization_ru = field(default='')
        taxpayer_organization_kz = field(default='')
        last_name_kz = field(default='')
        first_name_kz = field(default='')
        middle_name_kz = field(default='')
        last_name_ru = field(default='')
        first_name_ru = field(default='')
        middle_name_ru = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        owner_name_kz = field(default='')
        owner_name_ru = field(default='')
        economic_sector = field(default='')
        total_due = field(default='')
        sub_total_main = field(default='')
        sub_total_late_fee = field(default='')
        sub_total_fine = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdTaxArrears150



Список налогоплательщиков реорганизованных с нарушением норм Налогового кодекса
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Код в проекте: kgd_taxviolators

Формат: Excel

Ссылка: http://kgd.gov.kz/mobile_api/services/taxpayers_unreliable_exportexcel/TAX_ARREARS_150/KZ_ALL/fileName/list_TAX_ARREARS_150_KZ_ALL.xlsx

Класс-структура:

..  code-block:: python

   class TaxViolatorsRow:
        num = field(default='')
        bin = field(default='')
        rnn = field(default='')
        taxpayer_organization = field(default='')
        taxpayer_name = field(default='')
        owner_name = field(default='')
        owner_iin = field(default='')
        owner_rnn = field(default='')
        inspection_act_no = field(default='')
        inspection_date = field(default='')

Запуск из контейнера:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdTaxViolators
