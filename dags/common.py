from airflow.models import Variable

env_flag = Variable.get('ENVIRONMENT')
project_name = Variable.get('PROJECT_NAME')
platform = Variable.get('PLATFORM')

docker_url = 'unix://var/run/docker.sock'
image = 'elessarelfstone/tcomextetl'


if env_flag == 'dev' and platform == 'windows':
    docker_url = 'tcp://host.docker.internal:2375'

environment = {'FTP_HOST': Variable.get('FTP_HOST'), 'FTP_USER': Variable.get('FTP_USER'),
               'FTP_PASS': Variable.get('FTP_PASS'), 'FTP_PATH': Variable.get('FTP_PATH')}

run_params = {
    'task_id': 'docker_runner',
    'image': 'elessarelfstone/tcomextetl',
    'auto_remove': True,
    'network_mode': f'{project_name}_luigi-net',
    'environment': environment,
    'docker_url': docker_url
}


def build_command(module, task):
    return f'luigi --module {module} {task}'