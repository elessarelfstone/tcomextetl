from datetime import datetime

from airflow.models import DAG
from airflow.models import Variable
from airflow.operators.docker_operator import DockerOperator


test_dag = DAG(
    "test_dag",
    start_date=datetime(2022, 8, 14),
)

host = 'host.docker.internal'

docker_operator = DockerOperator(
    task_id="docker_command",
    image="elessarelfstone/tcomextetl",
    # command="/bin/sleep 5",
    command="luigi --module dgov_addrreg DgovAddrRegDGeonimsTypes",
    auto_remove=True,
    dag=test_dag,
    network_mode='tcomextetl_luigi-net',
    environment={'FTP_HOST': Variable.get('_FTP_HOST'), 'FTP_USER': Variable.get('_FTP_USER'),
                 'FTP_PASS': Variable.get('_FTP_PASS'), 'FTP_PATH': Variable.get('_FTP_PATH')},
    # docker_url='unix://var/run/docker.sock'
    docker_url=f'tcp://{host}:2375'
)


docker_operator
