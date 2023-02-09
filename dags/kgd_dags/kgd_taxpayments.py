import sys
from datetime import datetime, timedelta

from airflow.models import DAG, Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


with DAG(dag_id='kgd_taxpayments',
         catchup=False,
         start_date=datetime.today() - timedelta(1),
         schedule_interval='0 4 1 * *',
         tags=['kgdgov']
         ) as dag:

    kgd_taxpayments = Runner(
        task_id='kgd_taxpayments',
        luigi_module='kgd_api',
        luigi_task='KgdSoapApiTaxPayments',
        luigi_params=f'--resume --month {Runner.previous_month()}',
        env_vars={'KGD_SOAP_TOKEN': Variable.get('KGD_SOAP_TOKEN')},
        do_xcom_push=False
    )

    kgd_taxpayments
