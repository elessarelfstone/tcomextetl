import sys
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


def delta_period(frmt: str = '%Y-%m-%d'):
    n_days = int(Variable.get('GOSZAKUP_N_DAYS_DELTA'))
    start, end = Runner.n_days_delta_period(n_days, frmt)
    return start, end


def prepare_command_args(**context):
    ti = context["ti"]
    command_args = context["dag_run"].conf.get("command_args", '')
    if not command_args:
        s, e = delta_period()
        command_args = f'--no-resume --start-date {s} --end-date {e}'
    ti.xcom_push(key='command_args', value=command_args)
