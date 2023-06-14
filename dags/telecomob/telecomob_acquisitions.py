import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.telecomob.telecomob_common import prepare_command_args

with DAG(
        dag_id='telecomob_acquisitions',
        catchup=False,
        # start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['telecomob']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    telecomob_acquisitions = Runner(
        task_id='telecomob_acquisitions',
        luigi_module='telecomob',
        luigi_task='TelecomobYandexMetricaRepAcquisitions',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'TELECOMOB_YANDEX_METRICA_TOKEN': Variable.get('TELECOMOB_YANDEX_METRICA_TOKEN')},
        pool='telecomob',
        do_xcom_push=False
    )

    command_args >> telecomob_acquisitions
