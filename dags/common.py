import sys
from airflow.models import Variable

sys.path.append('.')

from dags.docker_runner import ExternalEtlDockerRunner as Runner


def delta_period(frmt: str = '%Y-%m-%d'):
    n_days_delta = int(Variable.get('SPEEDTEST_N_DAYS_DELTA'))
    start, end = Runner.n_days_delta_period(n_days_delta, frmt)
    return start, end
