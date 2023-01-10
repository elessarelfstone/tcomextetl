import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_kpved',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = '--no-resume'

    sgov_kpved = ExternalEtlDockerRunner(
        task_id='sgov_kpved',
        luigi_module='sgov_excel',
        luigi_task='SgovKpved',
        luigi_params=luigi_params,
        pool='sgov'
    )

    sgov_kpved
