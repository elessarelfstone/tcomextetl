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
        dag_id='nb_rates',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['national_bank']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    nb_rates = Runner(
        task_id='nb_rates',
        luigi_module='nationalbank',
        luigi_task='NBRates',
        do_xcom_push=False
    )

    command_args >> nb_rates
