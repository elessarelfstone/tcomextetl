import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='qualys_vulnerabilities',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='30 0 * * *',
        tags=['qualys']
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

    qualys_vulnerabilities = Runner(
        task_id='qualys_vulnerabilities',
        luigi_module='qualys',
        luigi_task='QualysVulnerabilities',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'QUALYS_API_USER': Variable.get('QUALYS_API_USER'),
                  'QUALYS_API_PASSWORD': Variable.get('QUALYS_API_PASSWORD')},
        pool='qualys',
        do_xcom_push=False
    )

    command_args >> qualys_vulnerabilities