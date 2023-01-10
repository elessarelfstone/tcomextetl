import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_juridical',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='0 6 13 * *',
         tags=['statgov']
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
