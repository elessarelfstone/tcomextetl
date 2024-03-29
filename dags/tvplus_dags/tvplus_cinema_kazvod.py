import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='tvplus_cinema_kazvod',
        catchup=False,
        start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['tvplus']
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

    tvplus_cinema_kazvod = Runner(
        task_id='tvplus_cinema_kazvod',
        luigi_module='tvplus',
        luigi_task='TvPlusCinemaKazvodCheckList',
        #luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        pool='tvplus',
        do_xcom_push=False
    )

    tvplus_cinema_kazvod