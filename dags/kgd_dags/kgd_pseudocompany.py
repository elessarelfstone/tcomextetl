import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_pseudocompany',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['kgdgov']
         ) as dag:

    luigi_params = '--no-resume'

    kgd_pseudocompany = ExternalEtlDockerRunner(
        task_id='kgd_pseudocompany',
        luigi_module='kgd_excel',
        luigi_task='KgdPseudoCompany',
        luigi_params=luigi_params,
        pool='kgd',
        do_xcom_push=False
    )

    kgd_pseudocompany
