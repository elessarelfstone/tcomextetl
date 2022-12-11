from datetime import datetime

from airflow.models import DAG

from docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_juridical',
         catchup=False,
         start_date=datetime(2022, 1, 1),
         schedule_interval='@monthly'
         ) as dag:

    sgov_links_prepare = ExternalEtlDockerRunner(
        task_id='sgov_links_prepare',
        luigi_module='sgov_excel',
        luigi_task='SgovRcutsPrepared'
    )

    sgov_rcuts_parse = ExternalEtlDockerRunner(
        task_id='sgov_rcuts_parse',
        luigi_module='sgov_excel',
        luigi_task='SgovRcutsJuridical'
    )

    sgov_links_prepare >> sgov_rcuts_parse
