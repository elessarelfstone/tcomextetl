

from tcomextetl.extract.http_requests import Downloader, HttpRequest


class SpeedTestDownloader(Downloader):

    def __init__(
        self,
        url,
        period: tuple,
        dataset: str,
        params=None,
        headers=None,
        auth=None,
        timeout=None
    ):
        super().__init__(url, params=params, headers=headers, auth=auth, timeout=timeout)
        self.dataset = dataset
        # self.url = url
        self.period = period

    def datafiles(self) -> list[dict]:
        files = []
        root = self.request(self.url).json()

        def _files(items):
            for item in items:
                if item['type'] == 'file' and item['name'].find('headers') == -1 and '_20' in item['name']:
                    dataset = item['name'][:item['name'].index('_20')]
                    date = str(item['name']).split('.')[0].split('_')[1]
                    # build list
                    if dataset == self.dataset:
                        files.append({
                            'dataset': dataset,
                            'name': item['name'],
                            # 'date': datetime.strptime(date, DEFAULT_FORMAT),
                            'date': date,
                            'url': item['url'],
                            'age': item['mtime']
                        })
                elif item['type'] == 'dir':
                    sub_items = self.request(f'{self.url}{item["url"]}').json()
                    _files(sub_items)

        _files(root)
        return files
