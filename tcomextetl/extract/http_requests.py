import re
import urllib3
from requests import Session
from requests.auth import HTTPBasicAuth


from tcomextetl.common.exceptions import ExternalSourceError
from tcomextetl.common.utils import pretty_size, FILE_FORMATS

# suppress warnings about insecure requests
# since we don't use certs mostly
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpRequest:
    def __init__(
        self,
        params=None,
        headers=None,
        auth=None,
        timeout=None,
        timeout_ban=None,
        verify_cert=False
    ):
        print(f"auth in begin of request code - {headers}")
        # verify always set in False
        # specifically for our company
        self.verify_cert = verify_cert

        if params:
            self.params = params
        else:
            self.params = {}

        self.headers = headers
        print(f"auth in request code - {self.headers}")
        self.auth = auth

        if auth and auth.get('user'):
            self.auth = HTTPBasicAuth(auth.get('user'), auth.get('password'))

        self._stat_meta_info = {}

        #read timeout
        self.timeout = timeout

        # timeout to avoid limitation on requests per time of source side
        self.timeout_ban = timeout_ban
        self.session = Session()

    def request(
        self,
        url: str,
        data=None,
        json=None,
        params=None,
        files=None,
        stream=False
    ):
        if data or json:
            method = 'POST'
        else:
            method = 'GET'

        p = self.params

        if params:
            p = {**self.params, **params}
        return self.session.request(
            method,
            url,
            params=p,
            files=files,
            data=data,
            json=json,
            headers=self.headers,
            timeout=self.timeout,
            auth=self.auth,
            stream=stream,
            verify=self.verify_cert
        )

    def head(self, url, params=None):
        return self.session.head(
            url,
            params=params,
            headers=self.headers,
            verify=self.verify_cert
        )


class Downloader(HttpRequest):

    def __init__(
        self,
        url,
        params=None,
        headers=None,
        auth=None,
        timeout=None,
        chunk_size=8192
    ):
        super().__init__(params, headers, auth, timeout)
        self.url = url
        self.chunk_size = chunk_size
        self._curr_size = 0

    @property
    def curr_size(self):
        return self._curr_size

    @property
    def status(self):
        return f'Downloaded {pretty_size(self.curr_size)}'

    @property
    def ext(self):
        _file_format = self._file_format(self.url)
        return _file_format['extension']

    def _file_format(self, url):

        ext = None
        file_format = None

        r = self.head(url, self.params)
        if r:
            content_type = r.headers.get('Content-Type')
            location = r.headers.get('Location')
            content_disposition = r.headers.get('Content-Disposition')

            _format = list(filter(lambda f: f['mime'] == content_type, FILE_FORMATS))

            if content_type and _format:
                file_format = _format.pop()

            elif content_disposition:
                file_name = re.findall('filename=(.+)', content_disposition)[0]
                ext = file_name.split('.')[-1]

            elif location:
                ext = location.split('.')[-1]

            if ext:
                _format = list(filter(lambda f: f['extension'] == ext, FILE_FORMATS))
                if _format:
                    file_format = _format.pop()

        return file_format

    def download(self, fpath, url=None):
        """ Download file using stream """

        _url = url if url else self.url

        file_format = self._file_format(_url)

        if not file_format:
            raise ExternalSourceError('Could not detect format of file')

        with self.request(_url, stream=True) as r:
            r.raise_for_status()
            f_size = 0
            with open(fpath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        f_size += len(chunk)

        return f_size

    def __iter__(self):

        r = self.request(self.url, stream=True)
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size=self.chunk_size):
            if chunk:
                self._curr_size += len(chunk)
                yield chunk
