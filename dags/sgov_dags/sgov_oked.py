import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_oked',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = '--no-resume'

    sgov_oked = ExternalEtlDockerRunner(
        task_id='sgov_oked',
        luigi_module='sgov_excel',
        luigi_task='SgovOked',
        luigi_params=luigi_params,
        pool='sgov',
        do_xcom_push=False
    )

    sgov_oked
