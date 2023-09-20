import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='mirapolis_online',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='0 1 * * *',
        tags=['mirapolis']
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

    mirapolis_online = Runner(
        task_id='mirapolis_online',
        luigi_module='mirapolis',
        luigi_task='MirapolisOnline',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'MIRAPOLIS_SECRET_KEY': Variable.get('MIRAPOLIS_SECRET_KEY')},
        pool='mirapolis',
        do_xcom_push=False
    )

    command_args >> mirapolis_online
