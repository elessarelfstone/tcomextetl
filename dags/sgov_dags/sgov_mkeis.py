import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_mkeis',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = ''

    sgov_mkeis = ExternalEtlDockerRunner(
        task_id='sgov_mkeis',
        luigi_module='sgov_excel',
        luigi_task='SgovMkeis',
        luigi_params=luigi_params,
        pool='sgov',
        do_xcom_push=False
    )

    sgov_mkeis
