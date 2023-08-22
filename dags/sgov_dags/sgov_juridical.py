import sys

import pendulum
from airflow.models import DAG, Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_juridical',
         catchup=False,
         start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='0 6 21 * *',
         tags=['statgov']
         ) as dag:

    sgov_rcuts_parse = ExternalEtlDockerRunner(
        task_id='sgov_rcuts_parse',
        luigi_module='sgov_excel',
        luigi_task='SgovRcutByKatoJuridical',
        do_xcom_push=False
    )

    sgov_rcuts_parse
