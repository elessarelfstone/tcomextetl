import sys

import pendulum as pm

sys.path.append('.')


def get_command_args(**context):
    """ Return string that are used as specified parameters to run Luigi tasks """
    ti = context["ti"]

    # execution date

    exec_date = pm.today().to_date_string()
    # exec_date = context["data_interval_end"].to_date_string()
    # print(f'{exec_date} - Date')
    command_args = context["dag_run"].conf.get("command_args", '')

    if not command_args:
        # n_days = context['params'].get('n_days_delta')
        n_days = context['n_days_delta']
        s = pm.today().subtract(days=n_days).to_date_string()
        e = pm.today().subtract(days=1).to_date_string()
        command_args = f'--start-date {s} --end-date {e} --date {exec_date}'

    ti.xcom_push(key='command_args', value=command_args)
