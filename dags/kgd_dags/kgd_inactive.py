import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_inactive',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['kgdgov']
         ) as dag:

    luigi_params = '--no-resume'

    kgd_inactive = ExternalEtlDockerRunner(
        task_id='kgd_inactive',
        luigi_module='kgd_excel',
        luigi_task='KgdInactive',
        luigi_params=luigi_params,
        pool='kgd',
        do_xcom_push=False
    )

    kgd_inactive
