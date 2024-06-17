import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='cloud_payments_no3ds',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['cloudpayments']
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

    cloudpayments_list = Runner(
        task_id='cloud_payments_no3ds',
        luigi_module='cloudpayments',
        luigi_task='CloudPaymentsNo3ds',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={
            'CLOUDPAYMENTS_NO3DS_USER': Variable.get('CLOUDPAYMENTS_NO3DS_USER'),
            'CLOUDPAYMENTS_NO3DS_PASS': Variable.get('CLOUDPAYMENTS_NO3DS_PASS'),
        },
        pool='cloudpayments',
        do_xcom_push=False
    )

    command_args >> cloudpayments_list
