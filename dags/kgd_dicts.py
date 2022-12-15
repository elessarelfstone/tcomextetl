from datetime import datetime

from airflow.models import DAG

from docker_runner import ExternalEtlDockerRunner


with DAG(dag_id='kgd_dicts',
         catchup=False,
         start_date=datetime(2022, 1, 1)
         ) as dag:

    luigi_params = ['--no-resume']

    kgd_bnkrp = ExternalEtlDockerRunner(
        task_id='kgd_bankrupt',
        luigi_module='kgd_excel',
        luigi_task='KgdBankrupt',
        luigi_params=luigi_params
    )

    kgd_inact = ExternalEtlDockerRunner(
        task_id='kgd_inactive',
        luigi_module='kgd_excel',
        luigi_task='KgdInactive',
        luigi_params=luigi_params
    )

    kgd_invreg = ExternalEtlDockerRunner(
        task_id='kgd_invregistration',
        luigi_module='kgd_excel',
        luigi_task='KgdInvregistration',
        luigi_params=luigi_params
    )

    kgd_jwaddr = ExternalEtlDockerRunner(
        task_id='kgd_jwrongaddress',
        luigi_module='kgd_excel',
        luigi_task='KgdWrongAddress',
        luigi_params=luigi_params
    )

    kgd_psdcmp = ExternalEtlDockerRunner(
        task_id='kgd_pseudocompany',
        luigi_module='kgd_excel',
        luigi_task='KgdPseudoCompany',
        luigi_params=luigi_params
    )

    kgd_txar150 = ExternalEtlDockerRunner(
        task_id='kgd_taxarrears150',
        luigi_module='kgd_excel',
        luigi_task='KgdTaxArrears150',
        luigi_params=luigi_params
    )

    kgd_taxviol = ExternalEtlDockerRunner(
        task_id='kgd_taxviolators',
        luigi_module='kgd_excel',
        luigi_task='KgdTaxViolators',
        luigi_params=luigi_params
    )

    kgd_bnkrp >> kgd_inact >> kgd_invreg >> kgd_jwaddr >> kgd_psdcmp >> kgd_txar150 >> kgd_taxviol
