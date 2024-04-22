import csv
import json
from math import floor
from datetime import datetime, timedelta
from time import sleep

import luigi
import pandas as pd
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from tasks.base import CsvFileOutput, FtpUploadedOutput, Runner
from tcomextetl.common.arch import extract_by_wildcard
from tcomextetl.common.csv import save_csvrows, dict_to_row, CSV_QUOTECHAR
from tcomextetl.common.dates import DEFAULT_FORMAT, n_days_ago
from tcomextetl.common.utils import build_fpath, append_file, rewrite_file
from tcomextetl.extract.aitu_requests import AituRequests, AituNotificationRequests
from settings import AITU_API_KEY, AITU_SECRET_KEY, AITU_PUSH_NOTIFICATIONS_PROJECT_ID, \
    AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID, AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY, AITU_PUSH_NOTIFICATIONS_CLIENT_ID

api_url = f"https://amplitude.com/api/2/export"
amplitude_id = 505199

scopes = ["https://www.googleapis.com/auth/cloud-platform"]
creds_dict = {
    "type": "service_account",
    "client_email": "kt-411@asiachat-8dd78.iam.gserviceaccount.com",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kt-411%40asiachat-8dd78.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
creds_dict = {
    "type": "service_account",
    "client_email": "kt-411@asiachat-8dd78.iam.gserviceaccount.com",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/kt-411%40asiachat-8dd78.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}
query = """SELECT * FROM `asiachat-8dd78.telecom.push_raw_data`"""
query_date = """WHERE TIMESTAMP_TRUNC(server_time, DAY) = TIMESTAMP("{}")"""


class AituOutput(CsvFileOutput):
    from_to = luigi.TupleParameter(default=())
    user = luigi.Parameter(default=AITU_API_KEY, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=AITU_SECRET_KEY, visibility=ParameterVisibility.HIDDEN)

    @property
    def auth(self):
        return {
            'user': self.user,
            'password': self.password
        }

    def run(self):
        params = {
            "start": self.from_to[0],
            "end": self.from_to[1]
        }

        parser = AituRequests(
            amplitude_id,
            api_url,
            params=params,
            auth=self.auth
        )

        for d in parser:
            save_csvrows(self.output_fpath,
                         [dict_to_row(_d, self.struct, '$') for _d in d],
                         quotechar='"')

            self.set_status_info(*parser.status_percent)

        rewrite_file(self.success_fpath, json.dumps(parser.stat))


@requires(AituOutput)
class AituFtpOutput(FtpUploadedOutput):
    pass


class AituRunner(Runner):
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AituRunner, self).params

        start = self.start_date.strftime('%Y%m%dT%H')
        end = (self.end_date + timedelta(days=1)).strftime('%Y%m%dT%H')

        params['from_to'] = (
            start,
            end
        )

        return params

    def requires(self):
        return AituFtpOutput(**self.params)


class AituLogs(AituRunner):
    name = luigi.Parameter('aitu_logs')


class AituNotificationOutput(CsvFileOutput):
    project_id = luigi.Parameter(default=AITU_PUSH_NOTIFICATIONS_PROJECT_ID, visibility=ParameterVisibility.HIDDEN)
    private_key_id = luigi.Parameter(default=AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY_ID,
                                     visibility=ParameterVisibility.HIDDEN)
    private_key = luigi.Parameter(default=AITU_PUSH_NOTIFICATIONS_PRIVATE_KEY, visibility=ParameterVisibility.HIDDEN)
    client_id = luigi.Parameter(default=AITU_PUSH_NOTIFICATIONS_CLIENT_ID, visibility=ParameterVisibility.HIDDEN)
    data_date = luigi.Parameter(default='')

    @property
    def request_sql(self):
        sql = query

        if self.data_date:
            query_format = query_date.format(self.data_date)
            sql = f"{query} {query_format}"

        return sql

    def run(self):
        creds_dict['project_id'] = self.project_id
        creds_dict['private_key_id'] = self.private_key_id
        creds_dict['private_key'] = self.private_key
        creds_dict['client_id'] = self.client_id

        parser = AituNotificationRequests(creds_dict, scopes, self.project_id, self.request_sql)

        df_aitu = parser.load()
        rows_count = 0

        if df_aitu:
            for row in df_aitu:
                aitu_row = dict(row)
                data = dict_to_row(aitu_row, self.struct)
                save_csvrows(self.output_fpath, [data], delimiter=';')
                rows_count += 1
        else:
            open(self.output_fpath, 'w').close()

        stat = parser.stat
        stat.update({'parsed': rows_count})
        rewrite_file(self.success_fpath, json.dumps(stat))


@requires(AituNotificationOutput)
class AituNotificationOutputFtpOutput(FtpUploadedOutput):
    pass


class AituNotificationRunner(Runner):
    name = luigi.Parameter()
    start_date = luigi.DateParameter(default=n_days_ago())
    end_date = luigi.DateParameter(default=n_days_ago())

    @property
    def params(self):
        params = super(AituNotificationRunner, self).params

        if not self.all_data:
            params['data_date'] = self.start_date.strftime(DEFAULT_FORMAT)

        return params

    def requires(self):
        return AituNotificationOutputFtpOutput(**self.params)


class AituNotification(AituNotificationRunner):
    name = luigi.Parameter('aitu_notifications')


if __name__ == '__main__':
    luigi.run()
