import sys

import pendulum
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args_for_prev_month


with DAG(dag_id='gosreestrkz_contact',
         catchup=False,
         start_date=pendulum.datetime(2024, 3, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='@monthly',
         tags=['gosreestrkz']
         ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=get_command_args_for_prev_month,
        dag=dag,
        do_xcom_push=False,
        op_kwargs={
            'n_days_delta': 1
        }
    )

    gosreestrkz_contact = Runner(
        task_id='gosreestrkz_contact',
        luigi_module='gosreestrkz',
        luigi_task='GosreestrKzContact',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'PROXY_FACTORY_USER': Variable.get('PROXY_FACTORY_USER'),
                  'PROXY_FACTORY_PASS': Variable.get('PROXY_FACTORY_PASS')},
        pool='gosreestrkz',
        do_xcom_push=False
    )

    command_args >> gosreestrkz_contact
