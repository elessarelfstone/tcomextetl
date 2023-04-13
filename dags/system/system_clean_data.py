import os
import sys
from pathlib import Path

from airflow.operators.python import PythonOperator
from airflow.models import DAG
from airflow.models import Variable

sys.path.append('.')

import pendulum


def clean_data_files():

    today = pendulum.today(tz=Variable.get('TZ'))
    red_line = today.subtract(days=int(Variable.get('N_DAYS_TO_CLEAN_DATA')))
    folder = Path(Variable.get('DATA_DIR'))

    for f in os.listdir(folder):
        f_nm_parts = f.split('.')[0].split('_')
        dt = f_nm_parts[-1]
        try:
            date = pendulum.from_format(dt, 'YYYYMMDD', tz=Variable.get('TZ'))
        except Exception:
            print(dt)

        if date < red_line:
            os.remove(folder.joinpath(f))


with DAG(
        dag_id='system_clean_data',
        catchup=False,
        start_date=pendulum.now(tz=f'{Variable.get("TZ")}').subtract(days=1),
        schedule_interval='@daily',
        tags=['system']
     ) as dag:

    clean_data = PythonOperator(
        task_id='clean_data',
        python_callable=clean_data_files,
        dag=dag,
        do_xcom_push=False
    )

    clean_data