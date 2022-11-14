import json
import logging
from datetime import datetime

# from common import run_params

from airflow.models import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator


# class MyDockerOperator(DockerOperator):
#     def __init__(self, module, luigi_task, **kwargs):
#         raw = " {{ dag_run.conf }} "
#         # with open('/opt/airflow/dags/test.txt', mode='w') as f:
#         #     f.write(raw)
#
#         # dag_run = json.loads(raw)
#         # print(dag_run)
#         period = " {{ dag_run.conf['period'] }} "
#         # period = kwargs['ti'].dag_run.conf['period']
#         # with open('/opt/airflow/dags/test.txt', mode='w') as f:
#         #     f.write(period)
#
#         # period = kwargs["dag_run"].conf.get('period')
#         c = f'luigi --module {module} {luigi_task} --period {period}'
#         super().__init__(command=c, **kwargs)
#
#
# with DAG(dag_id='dgov_addrreg',
#          catchup=False,
#          start_date=datetime(2022, 1, 1)
#          ) as dag:
#
#     period = "{{ dag_run.conf['period'] }}"
#
#     # with open('/opt/airflow/dags/test.txt', mode='w') as f:
#     #     f.write(period)
#     #
#     # docker_operator = DockerOperator(**run_params,
#     #                                  command='luigi --module dgov_addrreg DgovAddrRegDGeonimsTypes --period ' + period)
#
#     docker_operator = MyDockerOperator(module='dgov_addrreg', luigi_task='DgovAddrRegDGeonimsTypes', **run_params)
#
#     docker_operator


