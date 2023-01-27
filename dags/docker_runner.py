import logging
import platform
from datetime import date, timedelta

from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


class ExternalEtlDockerRunner(DockerOperator):

    template_fields = ("luigi_params",) + DockerOperator.template_fields

    def __init__(
        self,
        task_id: str,
        luigi_module: str,
        luigi_task: str,
        luigi_params: str = "",
        env_vars=None,
        **kwargs
    ):

        _vars = {
            'FTP_HOST': Variable.get('FTP_HOST'),
            'FTP_USER': Variable.get('FTP_USER'),
            'FTP_PASS': Variable.get('FTP_PASS'),
            'FTP_PATH': Variable.get('FTP_PATH'),
            'FTP_EXPORT_PATH': Variable.get('FTP_EXPORT_PATH'),
            'TBOT_TOKEN': Variable.get('TBOT_TOKEN'),
            'TBOT_CHAT_IDS': Variable.get('TBOT_CHAT_IDS')
        }

        _env = Variable.get('ENVIRONMENT')
        _platform = platform.system().lower()
        image = Variable.get('IMAGE')

        temp_mount_point = Mount(
            source=Variable.get('HOST_TEMP_DIR'),
            target='/temp',
            type="bind"
        )

        data_mount_point = Mount(
            source=Variable.get('HOST_DATA_DIR'),
            target='/data',
            type="bind"
        )

        docker_url = 'unix://var/run/docker.sock'

        if _env == 'dev' or _platform == 'windows':
            docker_url = 'tcp://host.docker.internal:2375'

        network_mode = '{}_{}'.format(Variable.get('PROJECT_NAME'), Variable.get('DOCKER_NETWORK'))

        if env_vars:
            _vars.update(env_vars)

        self.luigi_params = luigi_params
        command = f'luigi --module {luigi_module} {luigi_task} ' + self.luigi_params

        super().__init__(
             task_id=task_id,
             container_name=task_id,
             image=image,
             auto_remove=True,
             network_mode=network_mode,
             docker_url=docker_url,
             environment=_vars,
             mounts=[temp_mount_point, data_mount_point],
             mount_tmp_dir=False,
             command=command,
             **kwargs
        )

    @staticmethod
    def previous_month() -> str:
        t = date.today()
        ld = date(t.year, t.month, 1) - timedelta(days=1)
        return '{}-{:02}'.format(ld.year, ld.month)

    @staticmethod
    def n_days_delta_period(
            n_days: int = 1,
            frmt: str = '%Y-%m-%d'
    ):
        d = date.today()
        d1 = d - timedelta(n_days)
        d2 = d - timedelta(1)
        return d1.strftime(frmt), d2.strftime(frmt)
