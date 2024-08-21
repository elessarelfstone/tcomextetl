import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.dgov_dags.common import get_dict_command_args

with DAG(
        dag_id='dgov_datasets_mugedektigi_bar_adamdarga_arna',
        catchup=False,
        start_date=pendulum.datetime(2024, 3, 1, tz=f'{Variable.get("TZ")}'),
        schedule_interval='@monthly',
        tags=['dgov_datasets']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=get_dict_command_args,
        dag=dag,
        do_xcom_push=False,
    )

    dgov_datasets_mugedektigi_bar_adamdarga_arna = Runner(
        task_id='dgov_datasets_mugedektigi_bar_adamdarga_arna',
        luigi_module='dgov_datasets',
        luigi_task='DgovDatasetsMugedektigiBarAdamdargaArna',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'DATAGOV_TOKEN': Variable.get('DATAGOV_TOKEN')},
        pool='dgov_datasets',
        do_xcom_push=False
    )

    command_args >> dgov_datasets_mugedektigi_bar_adamdarga_arna