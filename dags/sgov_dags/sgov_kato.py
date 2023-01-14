import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_kato',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='@monthly',
         tags=['statgov']
         ) as dag:

    luigi_params = '--no-resume'

    sgov_kato = ExternalEtlDockerRunner(
        task_id='sgov_kato',
        luigi_module='sgov_excel',
        luigi_task='SgovKato',
        luigi_params=luigi_params,
        pool='sgov',
        do_xcom_push=False
    )

    sgov_kato
