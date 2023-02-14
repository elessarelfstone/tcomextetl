import sys
from datetime import datetime, timedelta

import pendulum
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_oked',
         catchup=False,
         # start_date=pendulum.datetime(2023, 1, 1, tz=f'{Variable.get("TZ")}'),
         start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(months=1),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = '--no-resume'

    sgov_oked = ExternalEtlDockerRunner(
        task_id='sgov_oked',
        luigi_module='sgov_excel',
        luigi_task='SgovOked',
        luigi_params=luigi_params,
        pool='sgov',
        do_xcom_push=False
    )

    sgov_oked
