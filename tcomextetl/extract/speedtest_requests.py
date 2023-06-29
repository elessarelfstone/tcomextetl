from datetime import datetime

import pandas as pd

from tcomextetl.common.dates import DEFAULT_FORMAT
from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.extract.http_requests import Downloader


class SpeedTestDownloader(Downloader):

    def __init__(
        self,
        url,
        start: str,
        end: str,
        dataset: str,
        params=None,
        headers=None,
        auth=None,
        timeout=None
    ):
        super().__init__(
            url,
            params=params,
            headers=headers,
            auth=auth,
            timeout=timeout
        )
        self.dataset = dataset

        all_files = self._all_files()

        dates_range = pd.date_range(
            datetime.strptime(start, DEFAULT_FORMAT),
            datetime.strptime(end, DEFAULT_FORMAT),
            freq='d'
        ).strftime('%Y-%m-%d').tolist()

        self._datafiles = []

        # filter dates
        for dt in dates_range:
            if dt not in [df['date'] for df in all_files]:
                raise ExternalSourceError(f'No data file for date - {dt}')
            else:
                self._datafiles.append(
                    list(filter(lambda df: df['date'] == dt, all_files)).pop()
                )

    def _all_files(self) -> list[dict]:

        files = []
        root = self.request(self.url).json()

        def _files(items):
            for item in items:
                # parse tree-like structure
                if item['type'] == 'file' and item['name'].find('headers') == -1 and '_20' in item['name']:
                    dataset = item['name'][:item['name'].index('_20')]
                    date = str(item['name']).split('.')[0].split('_')[1]
                    # build list
                    if dataset == self.dataset:
                        files.append({
                            'dataset': dataset,
                            'name': item['name'],
                            'date': date,
                            'url': item['url'],
                            'age': item['mtime']
                        })
                elif item['type'] == 'dir':
                    sub_items = self.request(f'{self.url}{item["url"]}').json()
                    _files(sub_items)

        # recursive call
        _files(root)
        return files

    @property
    def length(self):
        return len(self._datafiles)

    def __iter__(self):
        for file in self._datafiles:
            yield file
