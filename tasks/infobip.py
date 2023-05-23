import csv
import json
import os
from math import floor
from datetime import datetime, timedelta

import luigi
from luigi.parameter import ParameterVisibility
from luigi.util import requires

from settings import (INFOBIP_URL, INFOBIP_USER,
                      INFOBIP_PASSWORD, INFOBIP_TIMEOUT)

from tasks.base import ApiToCsv, FtpUploadedOutput, Runner, ExternalCsvLocalInput
from tcomextetl.common.csv import save_csvrows, dict_to_row
from tcomextetl.common.dates import DEFAULT_FORMAT

from tcomextetl.extract.infobip_requests import InfobipRestApiParser
from tcomextetl.common.utils import rewrite_file


class InfobipOutput(ApiToCsv):

    endpoint = luigi.Parameter()

    user = luigi.Parameter(default=INFOBIP_USER, visibility=ParameterVisibility.HIDDEN)
    password = luigi.Parameter(default=INFOBIP_PASSWORD, visibility=ParameterVisibility.HIDDEN)
    limit = luigi.IntParameter(default=100)

    from_to = luigi.TupleParameter(default=())
    timeout = luigi.IntParameter(default=1)
    timeout_ban = luigi.IntParameter(default=1)

    @property
    def url(self):
        return f'{INFOBIP_URL}{self.endpoint}'

    @property
    def request_params(self):
        params = dict(page=0, limit=self.limit)

        if self.from_to:
            u_after, u_before = self.from_to
            u_after = datetime.strptime(u_after, DEFAULT_FORMAT).isoformat() + '.000UTC'
            u_before = datetime.strptime(u_before, DEFAULT_FORMAT)
            u_before = u_before.replace(hour=23, minute=59, second=59).isoformat() + '.000UTC'
            params['updatedAfter'], params['updatedBefore'] = u_after, u_before
            print(params)

        # resume if there were fails
        if self.resume and os.path.exists(self.stat_fpath):
            next_page_params = self.stat['page_params']
            params.update(next_page_params)

        return params

    def run(self):
        auth = {'user': self.user, 'password': self.password}
        parser = InfobipRestApiParser(self.url, self.endpoint, params=self.request_params,
                                      auth=auth, timeout=self.timeout, timeout_ban=self.timeout_ban)

        # set parsed rows count if resume
        parser.set_parsed_count(self.stat.get('parsed', 0))

        for data in parser:
            save_csvrows(self.output_fpath,
                         [dict_to_row(d, self.struct) for d in data], quotechar='"')
            self.set_status_info(*parser.status_percent)
            stat = parser.stat
            stat.update(self.request_params)
            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(InfobipOutput)
class InfobipFtpOutput(FtpUploadedOutput):
    pass


class InfobipRunner(Runner):

    start_date = luigi.Parameter(default=Runner.yesterday())
    end_date = luigi.Parameter(default=Runner.yesterday())

    def requires(self):

        params = self.params

        if not self.all_data:
            params['from_to'] = (self.start_date, self.end_date)

        return InfobipFtpOutput(**params)


class InfobipAgents(InfobipRunner):

    name = luigi.Parameter('infobip_agents')


class InfobipQueues(InfobipRunner):

    name = luigi.Parameter('infobip_queues')


class InfobipConversations(InfobipRunner):

    name = luigi.Parameter('infobip_conversations')


class InfobipConversationDetailsOutput(InfobipOutput):

    conversation_id = None

    def requires(self):
        return ExternalCsvLocalInput(name='infobip_conversations')

    def _conv_ids(self):
        _ids = []
        with open(self.input().path, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.sep)
            for row in csv_reader:
                _ids.append(row[0])

        return _ids

    @property
    def request_params(self):
        params = super().request_params
        if self.endpoint == 'tags':
            params['conversationId'] = self.conversation_id

        return params

    @property
    def url(self):
        url = super().url
        if self.endpoint == 'messages':
            url = f'{INFOBIP_URL}conversations/{self.conversation_id}/messages'

        return url

    def run(self):
        auth = {'user': self.user, 'password': self.password}

        conv_ids = self._conv_ids()
        total_conv_ids = len(conv_ids)

        # if we resume start from the last conv_id we write in stat file
        if self.resume and self.request_params.get('conv_id'):
            conv_id = self.request_params['conv_id']
            conv_ids = conv_ids[conv_ids.index(conv_id)+1:]

        parsed_convs_count = self.stat.get('parsed_convs_count', 0)
        total_parsed = self.stat.get('parsed_convs_count', 0)

        for conv_id in conv_ids:
            self.conversation_id = conv_id
            params = self.request_params

            parser = InfobipRestApiParser(self.url, self.endpoint, params=params,
                                          auth=auth, timeout=self.timeout, timeout_ban=self.timeout_ban)

            for data in parser:
                _data = []

                for d in data:
                    _data.append({**d, **{'conversationid': conv_id}})

                save_csvrows(self.output_fpath,
                             [dict_to_row(d, self.struct) for d in _data], quotechar='"')

                total_parsed += len(data)

            parsed_convs_count += 1
            p = floor((parsed_convs_count * 100) / len(conv_ids))
            status = f'Total conversations: {len(conv_ids)}. Conversation ID: {conv_id}. \n'
            status += f'Parsed conversations: {parsed_convs_count}. Total rows parsed: {total_parsed}'

            self.set_status_info(status, p)
            stat = parser.stat
            stat.update(self.request_params)
            stat["total_conv_ids"] = total_conv_ids
            stat["total_parsed"] = total_parsed
            stat["parsed_convs_count"] = parsed_convs_count
            stat["conv_id"] = conv_id

            del stat["total"]
            del stat["parsed"]

            rewrite_file(self.stat_fpath, json.dumps(stat))

        self.finalize()


@requires(InfobipConversationDetailsOutput)
class InfobipConversationDetailsFtpOutput(FtpUploadedOutput):
    pass


class InfobipConversationDetailsRunner(InfobipRunner):

    def requires(self):
        params = self.params

        if not self.all_data:
            params['from_to'] = (self.start_date, self.end_date)

        return InfobipConversationDetailsFtpOutput(**params)


class InfobipMessages(InfobipConversationDetailsRunner):

    name = luigi.Parameter('infobip_messages')


class InfobipTags(InfobipConversationDetailsRunner):

    name = luigi.Parameter('infobip_tags')


if __name__ == '__main__':
    luigi.run()
