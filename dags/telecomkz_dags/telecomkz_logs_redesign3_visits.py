import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='telecomkz_logs_redesign3_visits',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='0 2 * * *',
        tags=['telecomkz']
) as dag:
    command_args = PythonOperator(
        task_id='command_args',
        python_callable=get_command_args,
        dag=dag,
        do_xcom_push=False,
        op_kwargs={
            'n_days_delta': 1
        }
    )

    telecomkz_logs_redesign3_visits = Runner(
        task_id='telecomkz_logs_redesign3_visits',
        luigi_module='telecomkz',
        luigi_task='TelecomkzYandexMetricaLogsRedesign3Visits',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'TELECOMKZ_YANDEX_METRICA_LOGS_REDESIGN3_TOKEN': Variable.get(
            'TELECOMKZ_YANDEX_METRICA_LOGS_REDESIGN3_TOKEN')},
        pool='telecomkz',
        do_xcom_push=False
    )

    command_args >> telecomkz_logs_redesign3_visits