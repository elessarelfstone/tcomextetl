import sys

from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

import pendulum
from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.goszakup_dags.goszakup_common import prepare_command_args

with DAG(
        dag_id='goszakup_plankato',
        catchup=False,
        # start_date=datetime.today() - timedelta(1),
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['goszakup']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    goszakup_plan_kato = Runner(
        task_id='goszakup_plan_kato',
        luigi_module='goszakup',
        luigi_task='GoszakupPlansKato',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'GOSZAKUP_TOKEN': Variable.get('GOSZAKUP_TOKEN')},
        pool='goszakup',
        do_xcom_push=False
    )

    command_args >> goszakup_plan_kato
