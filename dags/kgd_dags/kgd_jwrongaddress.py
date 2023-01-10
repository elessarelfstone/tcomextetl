import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_jwrongaddress',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['kgdgov']
         ) as dag:

    luigi_params = '--no-resume'

    kgd_jwrongaddress = ExternalEtlDockerRunner(
        task_id='kgd_jwrongaddress',
        luigi_module='kgd_excel',
        luigi_task='KgdWrongAddress',
        luigi_params=luigi_params,
        pool='kgd'
    )

    kgd_jwrongaddress
