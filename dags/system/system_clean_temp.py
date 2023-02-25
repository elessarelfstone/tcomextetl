import os
import sys
from pathlib import Path

from airflow.operators.bash import BashOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

import pendulum

folder = Path(Variable.get('TEMP_DIR'))

with DAG(
        dag_id='system_clean_temp',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(months=1),
        schedule_interval='@monthly',
        tags=['system']
     ) as dag:

    clean_data = BashOperator(
        task_id='clean_temp',
        bash_command=f'rm -rf {folder}/*',
        dag=dag,
        do_xcom_push=False
    )

    clean_data