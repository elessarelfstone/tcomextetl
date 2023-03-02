import sys
from datetime import datetime, timedelta

import pendulum
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_bankrupt',
         catchup=False,
         start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='@monthly',
         tags=['kgdgov']
         ) as dag:

    luigi_params = ''

    kgd_bankrupt = ExternalEtlDockerRunner(
        task_id='kgd_bankrupt',
        luigi_module='kgd_excel',
        luigi_task='KgdBankrupt',
        luigi_params=luigi_params,
        pool='kgd',
        do_xcom_push=False
    )

    kgd_bankrupt
