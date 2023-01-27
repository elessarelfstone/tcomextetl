import sys
from datetime import datetime, timedelta

from airflow.models import DAG

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_active_juridical',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='0 6 14 * *',
         tags=['statgov']
         ) as dag:

    sgov_links_active_prepare = ExternalEtlDockerRunner(
        task_id='sgov_links_active_prepare',
        luigi_module='sgov_excel',
        luigi_task='SgovRcutsActivePrepared'
    )

    sgov_rcuts_active_parse = ExternalEtlDockerRunner(
        task_id='sgov_rcuts_active_parse',
        luigi_module='sgov_excel',
        luigi_task='SgovRcutsActiveJuridical',
        do_xcom_push=False
    )

    sgov_links_active_prepare >> sgov_rcuts_active_parse
