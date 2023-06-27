import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.infobip_dags.infobip_common import prepare_command_args

with DAG(
        dag_id='infobip_conversations',
        catchup=False,
        start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['infobip']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=prepare_command_args,
        dag=dag,
        do_xcom_push=False
    )

    infobip_conversations = Runner(
        task_id='infobip_conversations',
        luigi_module='infobip',
        luigi_task='InfobipConversations',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'INFOBIP_USER': Variable.get('INFOBIP_USER'),
                  'INFOBIP_PASSWORD': Variable.get('INFOBIP_PASSWORD')},
        pool='infobip',
        do_xcom_push=False
    )

    command_args >> infobip_conversations
