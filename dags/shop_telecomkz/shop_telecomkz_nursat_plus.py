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
        dag_id='shop_telecomkz_nursat_plus',
        catchup=False,
        start_date=pendulum.datetime(2024, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['shop_telecomkz']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    shop_telecomkz_nursat_plus = Runner(
        task_id='shop_telecomkz_nursat_plus',
        luigi_module='shop_telecomkz',
        luigi_task='ShopTelecomKzNursatPlus',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'SHOP_TELECOMKZ_NURSAT_PLUS_TOKEN': Variable.get('SHOP_TELECOMKZ_NURSAT_PLUS_TOKEN')},
        pool='shop_telecomkz',
        do_xcom_push=False
    )

    command_args >> shop_telecomkz_nursat_plus
