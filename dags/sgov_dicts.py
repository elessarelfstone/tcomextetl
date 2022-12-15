from datetime import datetime

from airflow.models import DAG

from docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='sgov_dicts',
         catchup=False,
         start_date=datetime(2022, 1, 1)
         ) as dag:

    luigi_params = ['--no-resume']

    sgov_kurk = ExternalEtlDockerRunner(
        task_id='sgov_kurk',
        luigi_module='sgov_excel',
        luigi_task='SgovKurk',
        luigi_params=luigi_params
    )

    sgov_oked = ExternalEtlDockerRunner(
        task_id='sgov_oked',
        luigi_module='sgov_excel',
        luigi_task='SgovOked',
        luigi_params=luigi_params
    )

    sgov_kato = ExternalEtlDockerRunner(
        task_id='sgov_kato',
        luigi_module='sgov_excel',
        luigi_task='SgovKato',
        luigi_params=luigi_params
    )

    sgov_mkeis = ExternalEtlDockerRunner(
        task_id='sgov_mkeis',
        luigi_module='sgov_excel',
        luigi_task='SgovMkeis',
        luigi_params=luigi_params
    )

    sgov_kpved = ExternalEtlDockerRunner(
        task_id='sgov_kpved',
        luigi_module='sgov_excel',
        luigi_task='SgovKpved',
        luigi_params=luigi_params
    )

    sgov_kurk >> sgov_oked >> sgov_kato >> sgov_mkeis >> sgov_kpved
