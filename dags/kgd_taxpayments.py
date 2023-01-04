from datetime import datetime

from airflow.models import DAG, Variable

from docker_runner import ExternalEtlDockerRunner as Runner


with DAG(dag_id='kgd_taxpayments',
         catchup=False,
         start_date=datetime(2022, 1, 1),
         schedule_interval='0 4 1 * *'
         ) as dag:

    kgd_taxpayments = Runner(
        task_id='kgd_taxpayments',
        luigi_module='kgd_api',
        luigi_task='KgdSoapApiTaxPayments',
        luigi_params=f'--month {Runner.previous_month()}',
        env_vars={'KGD_SOAP_TOKEN': Variable.get('KGD_SOAP_TOKEN')}
    )

    kgd_taxpayments
