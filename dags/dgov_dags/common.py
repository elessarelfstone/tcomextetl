import sys

from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


def get_command_args(**context):
    ti = context["ti"]
    command_args = context["dag_run"].conf.get("command_args", '')
    ti.xcom_push(key='command_args', value=command_args)


def get_dict_command_args(**context):
    ti = context["ti"]
    command_args = context["dag_run"].conf.get("command_args", '')

    if not command_args:
        command_args = f'--all-data'

    ti.xcom_push(key='command_args', value=command_args)
