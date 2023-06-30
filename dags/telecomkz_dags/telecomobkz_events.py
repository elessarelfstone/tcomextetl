import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.telecomkz_dags.telecomobkz_common import prepare_command_args

with DAG(
        dag_id='telecomobkz_events',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['telecomobkz']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    telecomobkz_events = Runner(
        task_id='telecomobkz_events',
        luigi_module='telecomkz',
        luigi_task='TelecomobkzYandexMetricaRepEvents',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN': Variable.get('TELECOMOBKZ_YANDEX_APP_METRICA_TOKEN')},
        pool='telecomobkz',
        do_xcom_push=False
    )

    command_args >> telecomobkz_events
