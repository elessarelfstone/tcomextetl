import sys

import pendulum
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner

with DAG(
        dag_id='infobip_omni_queues',
        catchup=False,
        start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@daily',
        tags=['infobip']
     ) as dag:

    infobip_omni_queues = Runner(
        task_id='infobip_omni_queues',
        luigi_module='infobip',
        luigi_task='InfobipOmniQueues',
        luigi_params="--all-data",
        env_vars={'INFOBIP_DRB_TOKEN': Variable.get('INFOBIP_DRB_TOKEN')},
        pool='infobip_omni',
        do_xcom_push=False
    )

    infobip_omni_queues
