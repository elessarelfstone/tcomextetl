import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='aitu_logs',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='0 1 * * *',
        tags=['aitu']
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

    aitu_logs = Runner(
        task_id='aitu_logs',
        luigi_module='aitu',
        luigi_task='AituLogs',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'AITU_API_KEY': Variable.get('AITU_API_KEY'),
                  'AITU_SECRET_KEY': Variable.get('AITU_SECRET_KEY')},
        pool='aitu',
        do_xcom_push=False
    )

    command_args >> aitu_logs
