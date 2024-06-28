import sys

import pendulum
from airflow.models import DAG, Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='goszakup_ref_fkrb_subprogram',
         catchup=False,
         start_date=pendulum.datetime(2023, 2, 1, tz=f'{Variable.get("TZ")}'),
         schedule_interval='@monthly',
         tags=['goszakup']
         ) as dag:

    luigi_params = ''

    goszakup_ref_fkrb_subprogram = ExternalEtlDockerRunner(
        task_id='goszakup_ref_fkrb_subprogram',
        luigi_module='goszakup',
        luigi_task='GoszakupRefFkrbSubProgram',
        luigi_params=luigi_params,
        pool='goszakup',
        env_vars={'GOSZAKUP_TOKEN': Variable.get('GOSZAKUP_TOKEN')},
        do_xcom_push=False
    )

    goszakup_ref_fkrb_subprogram