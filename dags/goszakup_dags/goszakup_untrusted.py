import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG, Variable


sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


with DAG(
        dag_id='goszakup_untrusted',
        catchup=False,
        start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@monthly',
        tags=['goszakup']
     ) as dag:

    goszakup_untrusted = Runner(
        task_id='goszakup_untrusted',
        luigi_module='goszakup',
        luigi_task='GoszakupUntrusted',
        luigi_params="--use-rest",
        env_vars={'GOSZAKUP_TOKEN': Variable.get('GOSZAKUP_TOKEN')},
        do_xcom_push=False
    )

    goszakup_untrusted
