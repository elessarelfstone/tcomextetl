Реестры сайта Комитета Государственных Доходов РК
-------------------------------------------------


Реестр налогоплательщиков признанных банкротами
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

