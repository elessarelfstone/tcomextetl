import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner

with DAG(
        dag_id='infobip_omni_agents',
        catchup=False,
        start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['infobip']
     ) as dag:

    infobip_omni_agents = Runner(
        task_id='infobip_omni_agents',
        luigi_module='infobip',
        luigi_task='InfobipOmniAgents',
        luigi_params="--all-data",
        env_vars={'INFOBIP_DRB_TOKEN': Variable.get('INFOBIP_DRB_TOKEN')},
        pool='infobip',
        do_xcom_push=False
    )

    infobip_omni_agents
