================
Описание проекта
================

**TCOMEXTETL** - Набор пайпланов для выгрузки данных с внешних источников в рамках  проекта BigData АО Казахтелеком.

Проект можно разделить на две логические части.

- Пайплайны на базе батч-оркестратора Luigi, непосредственно выполняющие ETL(парсинг, маппинг с классами-структурами, трансформация, сохранение на FTP и т.д. )
- Набор пайплайнов(DAGs) на базе Airflow для обеспечения планирования(шедуллинга) выполнения джобов.

Папка tcomextetl содержит в себе программный код выполняющий основные ETL операции по работе с данными, осуществляющий HTTP взаимодействие и прочие вспомогательные функции. Пайплайны с тасками Luigi находятся с папке tasks. Описание разбито по источникам:

- `Справочники и классификаторы сайта stat.gov.kz <https://github.com/elessarelfstone/tcomextetl/blob/master/docs/sgov_excel.rst>`_
- `Реестры сайта Комитета Гос. Доходов РК <https://github.com/elessarelfstone/tcomextetl/blob/master/docs/kgd_excel.rst>`_
- `Унифицированные сервисы с данными по государственным закупкам <https://github.com/elessarelfstone/tcomextetl/blob/master/docs/goszakup.rst>`_


Запуск пайплайнов из контейнеров
--------------------------------

Для запуска пайплайнов из докер-контейнеров необходимо предварительно

1. Создать следующие директории в домашней директории вашего пользователя:

..  code-block:: bash

    mkdir ~/data ~/temp

2. Загрузить compose-файл:

..  code-block:: bash

    wget https://raw.githubusercontent.com/elessarelfstone/tcomextetl/master/docker-compose.home.yml -o docker-compose.home.yml

3. Развернуть окружение через команду docker-compose

..  code-block:: bash

    docker-compose -f docker-compose.home.yml up -d --scale job=0


В результате в контейнерах будут развернуты диспетчер Luigi и FTP сервер. Диспетчер Luigi предназначен исключительно
для управления процессом выполения пайплайна(граф выполнения, зависимости, распределение ресурсов, статусы и т.д.)


Далее собственно запускаем конкретный пайплайн, используя тот же docker-compose. Ниже приведен пример запуска пайплайна выгружающего
список налогоплательщиков признанных банкротами:

..  code-block:: bash

    docker-compose -f docker-compose.home.yml run --rm job luigi --module kgd_excel KgdBankrupt

Посмотреть некоторые детали выполнения можно через Web-интерфейс по адресу:

..  code-block:: bash

    https://<host>:8082

Если вы запускаете локально:

..  code-block:: bash

    https://localhost:8082

