from datetime import datetime

from airflow.models import DAG
from airflow.models import Variable

from docker_runner import ExternalEtlDockerRunner


with DAG(
        dag_id='goszakup_companies',
        catchup=False,
        start_date=datetime(2022, 12, 11),
        # schedule_interval='50 18 * * *'
     ) as dag:

    goszakup_companies = ExternalEtlDockerRunner(
        task_id='goszakup_companies',
        luigi_module='goszakup',
        luigi_task='GoszakupCompanies',
        luigi_params=['--no-resume'],
        env_vars={'GOSZAKUP_TOKEN': Variable.get('GOSZAKUP_TOKEN')}
    )

    goszakup_companies
