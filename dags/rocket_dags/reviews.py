import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='rocketdata_reviews',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='0 7 * * *',
        tags=['rocketdata']
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

    reviews = Runner(
        task_id='rocketdata_reviews',
        luigi_module='rocketdata',
        luigi_task='RocketDataReviews',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        do_xcom_push=False,
        pool='rocketdata',
        env_vars={'ROCKETDATA_TOKEN': Variable.get('ROCKETDATA_TOKEN')}
    )

    command_args >> reviews
