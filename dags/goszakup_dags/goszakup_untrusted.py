import sys
from datetime import datetime, timedelta

from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


with DAG(
        dag_id='goszakup_untrusted',
        catchup=False,
        start_date=datetime.today() - timedelta(1),
        schedule_interval='0 6 * * *',
        tags=['goszakup']
     ) as dag:

    goszakup_untrusted = Runner(
        task_id='goszakup_untrusted',
        luigi_module='goszakup',
        luigi_task='GoszakupUntrusted',
        luigi_params="--use-rest",
        env_vars={'GOSZAKUP_TOKEN': Variable.get('GOSZAKUP_TOKEN')},
        do_xcom_push=False
    )

    goszakup_untrusted
