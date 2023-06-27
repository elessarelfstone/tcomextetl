import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.speedtest_dags.speedtest_common import prepare_command_args

with DAG(
        dag_id='speedtest_fixed_network_performance',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['speedtest']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    speedtest_sensitive_data = Runner(
        task_id='speedtest_fixed_network_performance',
        luigi_module='speedtest',
        luigi_task='SpeedtestSensitiveData',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={
            'SPEEDTEST_USER': Variable.get('SPEEDTEST_USER'),
            'SPEEDTEST_PASS': Variable.get('SPEEDTEST_PASS')
        },
        pool='speedtest',
        do_xcom_push=False
    )

    command_args >> speedtest_sensitive_data
