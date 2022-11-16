import platform

from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


class ExternalEtlDockerRunner(DockerOperator):
    def __init__(self, task_id, luigi_module, luigi_task, env_vars=None, **kwargs):

        _vars = {'FTP_HOST': Variable.get('FTP_HOST'), 'FTP_USER': Variable.get('FTP_USER'),
                 'FTP_PASS': Variable.get('FTP_PASS'), 'FTP_PATH': Variable.get('FTP_PATH')}

        _env = Variable.get('ENVIRONMENT')
        _platform = platform.system().lower()
        image = Variable.get('IMAGE')

        # mounts = None
        # if _env == 'prod':
        mounts = Mount(
            source='/tmp/',
            target='/tmp/'
        )

        if _env == 'dev' or _platform == 'windows':
            docker_url = 'tcp://host.docker.internal:2375'
        else:
            docker_url = 'unix://var/run/docker.sock'

        network_mode = '{}_{}'.format(Variable.get('PROJECT_NAME'), Variable.get('DOCKER_NETWORK'))

        if env_vars:
            _vars.update(env_vars)

        command = f'luigi --module {luigi_module} {luigi_task} ' + "{{ dag_run.conf.get('command_args', '') }}"

        super().__init__(
                         task_id=task_id,
                         container_name=task_id,
                         image=image,
                         auto_remove=True,
                         network_mode=network_mode,
                         docker_url=docker_url,
                         environment=_vars,
                         mounts=[mounts],
                         mount_tmp_dir=False,
                         command=command, **kwargs
        )
