from __future__ import annotations

import urllib3
from abc import ABC, abstractmethod
from collections.abc import Iterator

from requests import Session, Response
from requests.auth import HTTPBasicAuth

# suppress warnings about insecure requests
# since we don't use certs mostly
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ExternalSourceError(Exception):
    pass


class DotDict:
    def __init__(self, initial_dict=None):
        self._dict = initial_dict or {}

    def __getattr__(self, item):
        if item in self._dict:
            if isinstance(self._dict[item], dict):
                return DotDict(self._dict[item])
            return self._dict[item]
        raise AttributeError(f"No such attribute: {item}")

    def __setattr__(self, key, value):
        if key == "_dict":
            super().__setattr__(key, value)
        else:
            self._dict[key] = value

    def __delattr__(self, item):
        if item in self._dict:
            del self._dict[item]
        else:
            raise AttributeError(f"No such attribute: {item}")

    def to_dict(self):
        return self._dict


class FlattenedDict:

    def __init__(self, sep: str = '_'):
        self._sep = sep

    def _flatten(self, _dict: dict) -> dict:

        out = {}

        def flatten(x, name=''):

            # another deep dive for nested dict
            if type(x) is dict:
                for a in x:
                    flatten(x[a], a)
            elif type(x) is list:
                # iterate over nested list
                i = 0
                _x = [True if type(i) in [list, dict] else False for i in x]
                if all(_x):
                    for a in x:
                        # build new key for each item in list
                        flatten(a, name + str(i) + self._sep)
                        i += 1
                else:
                    out[name] = x
            else:
                out[name] = x

        flatten(_dict)

        return out

    def _clean(self, _dict: dict) -> dict:
        exclusion_chars = f'{self._sep}0123456789'
        return {k.lstrip(exclusion_chars): v for k, v in _dict.items()}

    def __call__(self, _dict: dict) -> dict:
        return self._clean(self._flatten(_dict))


class HttpRequest:
    def __init__(
        self,
        params: dict | None = None,
        headers: dict | None = None,
        auth: dict | None = None,
        timeout: int | float | None = None,
        verify_cert: bool = False
    ):

        self.verify_cert = verify_cert

        if params:
            self.params = params
        else:
            self.params = {}

        self.headers = headers
        self.auth = auth

        if auth and auth.get('user'):
            self.auth = HTTPBasicAuth(auth.get('user'), auth.get('password'))

        self.timeout = timeout
        self.session = Session()

    def request(
        self,
        url: str,
        data: str | dict | None = None,
        json: dict | None = None,
        params: dict | None = None,
        files: list | None = None,
        stream: bool = False
    ) -> Response:

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

    def head(self, url: str, params: dict | None = None) -> Response:

        return self.session.head(
            url,
            params=params,
            headers=self.headers,
            verify=self.verify_cert
        )


class BaseDataPlugin(ABC):

    @abstractmethod
    def __init__(self, context: dict):
        self._raw = None
        self._context = context

    @property
    def context(self):
        return DotDict(self._context)

    @abstractmethod
    def data(self, meta: dict | None = None) -> Iterator[list[dict]]:
        pass

    @abstractmethod
    def stat(self) -> dict:
        pass

    # @abstractmethod
    # def _load(self) -> dict:
    #     pass

    @abstractmethod
    def _parse(self) -> list[dict]:
        pass

    @abstractmethod
    def progress_status(self) -> tuple[int, str]:
        pass

    def scheme_validate(self, data: list[tuple]):
        pass



