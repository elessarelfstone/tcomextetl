import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='amplitude_loyalty_program_logs',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='0 2 * * *',
        tags=['amplitude']
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

    amplitude_loyalty_program_logs = Runner(
        task_id='amplitude_loyalty_program_logs',
        luigi_module='amplitude',
        luigi_task='AmplitudeLoyaltyProgramLogs',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'AMPLITUDE_LOYALTY_PROGRAM_LOGS_API_KEY': Variable.get('AMPLITUDE_LOYALTY_PROGRAM_LOGS_API_KEY'),
                  'AMPLITUDE_LOYALTY_PROGRAM_LOGS_SECRET_KEY': Variable.get('AMPLITUDE_LOYALTY_PROGRAM_LOGS_SECRET_KEY')},
        pool='amplitude',
        do_xcom_push=False
    )

    command_args >> amplitude_loyalty_program_logs
