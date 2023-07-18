import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='crmsensor_checklist',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['crmsensor']
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

    crmsensor_checklist = Runner(
        task_id='crmsensor_checklist',
        luigi_module='crmsensor',
        luigi_task='CrmsensorCheckList',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={
            'CRMSENSOR_USER': Variable.get('CRMSENSOR_USER'),
            'CRMSENSOR_PASS': Variable.get('CRMSENSOR_PASS')
        },
        pool='crmsensor',
        do_xcom_push=False
    )

    command_args >> crmsensor_checklist
