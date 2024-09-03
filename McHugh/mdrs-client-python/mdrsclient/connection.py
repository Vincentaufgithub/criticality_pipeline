import platform
import threading
from typing import TypedDict

from requests import Response, Session
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Unpack is new in 3.11
from typing_extensions import Unpack

from mdrsclient.__version__ import __version__
from mdrsclient.cache import CacheFile
from mdrsclient.exceptions import MissingConfigurationException
from mdrsclient.models import Laboratories, Token, User


class _KwArgsMDRSConnectionGet(TypedDict, total=False):
    params: dict[str, str | int]
    stream: bool


class _KwArgsMDRSConnectionPost(TypedDict, total=False):
    params: dict[str, str | int]
    data: dict[str, str | int] | MultipartEncoder
    headers: dict[str, str]


class _KwArgsMDRSConnectionPut(TypedDict, total=False):
    params: dict[str, str | int]
    data: dict[str, str | int] | MultipartEncoder
    headers: dict[str, str]


class _KwArgsMDRSConnectionDelete(TypedDict, total=False):
    params: dict[str, str | int]


class MDRSConnection:
    url: str
    session: Session
    lock: threading.Lock
    __cache: CacheFile

    def __init__(self, remote: str, url: str) -> None:
        super().__init__()
        self.url = url
        self.session = Session()
        self.lock = threading.Lock()
        self.__cache = CacheFile(remote)
        self.__prepare_headers()

    def get(self, url: str, **kwargs: Unpack[_KwArgsMDRSConnectionGet]) -> Response:
        return self.session.get(self.__build_url(url), **kwargs)

    def post(self, url: str, **kwargs: Unpack[_KwArgsMDRSConnectionPost]) -> Response:
        return self.session.post(self.__build_url(url), **kwargs)

    def put(self, url: str, **kwargs: Unpack[_KwArgsMDRSConnectionPut]) -> Response:
        return self.session.put(self.__build_url(url), **kwargs)

    def delete(self, url: str, **kwargs: Unpack[_KwArgsMDRSConnectionDelete]) -> Response:
        return self.session.delete(self.__build_url(url), **kwargs)

    def logout(self) -> None:
        del self.__cache.user
        del self.__cache.token
        self.session.headers.update({"Authorization": ""})

    @property
    def user(self) -> User | None:
        return self.__cache.user

    @user.setter
    def user(self, user: User) -> None:
        self.__cache.user = user

    @property
    def token(self) -> Token | None:
        return self.__cache.token

    @token.setter
    def token(self, token: Token) -> None:
        self.__cache.token = token
        self.__prepare_headers()

    @property
    def laboratories(self) -> Laboratories:
        return self.__cache.laboratories

    @laboratories.setter
    def laboratories(self, laboratories: Laboratories) -> None:
        self.__cache.laboratories = laboratories

    def __build_url(self, path: str) -> str:
        if self.url == "":
            raise MissingConfigurationException("remote host is not configured")
        return f"{self.url}/{path}"

    def __prepare_headers(self) -> None:
        self.session.headers.update(
            {
                "User-Agent": f"MdrsClient/{__version__} (Python {platform.python_version()} - {platform.platform()})",
                "Accept": "application/json",
            }
        )
        if self.token is not None:
            self.session.headers.update({"Authorization": f"Bearer {self.token.access}"})
