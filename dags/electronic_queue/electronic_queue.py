import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.goszakup_dags.goszakup_common import prepare_command_args

with DAG(
        dag_id='electronic_queue',
        catchup=False,
        start_date=pendulum.datetime(2024, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['electronic_queue']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    electronic_queue = Runner(
        task_id='electronic_queue',
        luigi_module='electronic_queue',
        luigi_task='ElectronicQueue',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'ELECTRONIC_QUEUE_LOGIN': Variable.get('ELECTRONIC_QUEUE_LOGIN'),
                  'ELECTRONIC_QUEUE_PASSWORD': Variable.get('ELECTRONIC_QUEUE_PASSWORD')},
        pool='electronic_queue',
        do_xcom_push=False
    )

    command_args >> electronic_queue