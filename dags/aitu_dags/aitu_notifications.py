import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='aitu_notifications',
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

    aitu_notifications = Runner(
        task_id='aitu_notifications',
        luigi_module='aitu',
        luigi_task='AituNotification',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'AITU_PUSH_NOTIFICATIONS_PROJECT_ID': Variable.get('AITU_PUSH_NOTIFICATIONS_PROJECT_ID'),
                  'AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID': Variable.get('AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID'),
                  'AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY': Variable.get('AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY'),
                  'AITU_PUSH_NOTIFICATIONS_CLIENT_ID': Variable.get('AITU_PUSH_NOTIFICATIONS_CLIENT_ID')},
        pool='aitu',
        do_xcom_push=False
    )

    command_args >> aitu_notifications
