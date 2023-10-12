import sys

import pendulum
from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner
from dags.common import get_command_args

with DAG(
        dag_id='samruk_contract_item_deliveries',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['samruk']
     ) as dag:

    command_args = PythonOperator(
        task_id='command_args',
        python_callable=get_command_args,
        dag=dag,
        do_xcom_push=False,
        op_kwargs={
            'n_days_delta': 3
        }
    )

    samruk_contract_item_deliveries = Runner(
        task_id='samruk_contract_item_deliveries',
        luigi_module='samruk',
        luigi_task='SamrukContractItemDeliveries',
        luigi_params="{{ task_instance.xcom_pull(task_ids='command_args', key='command_args') }}",
        env_vars={'SAMRUK_TOKEN': Variable.get('SAMRUK_TOKEN'),
                  'SAMRUK_API_HOST': Variable.get('SAMRUK_API_HOST')
                  },
        pool='samruk',
        do_xcom_push=False
    )

    command_args >> samruk_contract_item_deliveries
