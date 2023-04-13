import sys

import pendulum
from airflow.models import DAG, Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_kurk',
         catchup=False,
         start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = ''

    sgov_kurk = ExternalEtlDockerRunner(
        task_id='sgov_kurk',
        luigi_module='sgov_excel',
        luigi_task='SgovKurk',
        luigi_params=luigi_params,
        pool='sgov',
        do_xcom_push=False
    )

    sgov_kurk
