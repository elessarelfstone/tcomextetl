from datetime import datetime

from airflow.models import DAG

from docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_kurk',
         catchup=False,
         start_date=datetime(2022, 1, 1)
         ) as dag:

    sgov_kurk = ExternalEtlDockerRunner(
        task_id='sgov_kurk',
        luigi_module='sgov_excel',
        luigi_task='SgovKurk'
    )

    sgov_kurk
