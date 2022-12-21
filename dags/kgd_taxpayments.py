from datetime import datetime

from airflow.models import DAG

from docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_taxpayments',
         catchup=False,
         start_date=datetime(2022, 1, 1)
         ) as dag:

    kgd_taxpayments = ExternalEtlDockerRunner(
        task_id='kgd_taxpayments',
        luigi_module='kgd_api',
        luigi_task='KgdSoapApiTaxPayments'
    )

    kgd_taxpayments
