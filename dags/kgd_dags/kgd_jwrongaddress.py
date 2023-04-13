import sys

import pendulum
from airflow.models import DAG, Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_jwrongaddress',
         catchup=False,
         start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='@monthly',
         tags=['kgdgov']
         ) as dag:

    luigi_params = ''

    kgd_jwrongaddress = ExternalEtlDockerRunner(
        task_id='kgd_jwrongaddress',
        luigi_module='kgd_excel',
        luigi_task='KgdWrongAddress',
        luigi_params=luigi_params,
        pool='kgd',
        do_xcom_push=False
    )

    kgd_jwrongaddress
