import sys
from datetime import datetime, timedelta

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable
from airflow.sensors.external_task import ExternalTaskSensor

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.infobip.infobip_common import prepare_command_args

with DAG(
        dag_id='infobip_messages',
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

    conversation_sensor = ExternalTaskSensor(
        task_id="conversation_sensor_id",
        external_dag_id="infobip_conversations",
        external_task_id="infobip_conversations",
        failed_states=['failed', 'skipped'],
        timeout=60 * 120,
        poke_interval=60 * 5,
        dag=dag
    )

    infobip_messages = Runner(
        task_id='infobip_messages',
        luigi_module='infobip',
        luigi_task='InfobipMessages',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'INFOBIP_USER': Variable.get('INFOBIP_USER'),
                  'INFOBIP_PASSWORD': Variable.get('INFOBIP_PASSWORD')},
        pool='infobip',
        do_xcom_push=False
    )

    conversation_sensor >> command_args >> infobip_messages