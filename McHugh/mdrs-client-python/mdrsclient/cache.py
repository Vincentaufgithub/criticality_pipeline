import dataclasses
import hashlib
import json
import os

from pydantic import TypeAdapter, ValidationError
from pydantic.dataclasses import dataclass

from mdrsclient.exceptions import UnexpectedException
from mdrsclient.models import Laboratories, Token, User
from mdrsclient.settings import CONFIG_DIRNAME
from mdrsclient.utils import FileLock


@dataclass
class CacheData:
    user: User | None = None
    token: Token | None = None
    laboratories: Laboratories = Laboratories()
    digest: str = ""

    def clear(self) -> None:
        self.user = None
        self.token = None
        self.laboratories.clear()
        self.digest = ""

    def update_digest(self) -> None:
        self.digest = self.__calc_digest()

    def verify_digest(self) -> bool:
        return self.digest == self.__calc_digest()

    def __calc_digest(self) -> str:
        return hashlib.sha256(
            json.dumps(
                [
                    None if self.user is None else dataclasses.asdict(self.user),
                    None if self.token is None else dataclasses.asdict(self.token),
                    dataclasses.asdict(self.laboratories),
                ]
            ).encode("utf-8")
        ).hexdigest()


class CacheFile:
    __serial: int
    __cache_dir: str
    __cache_file: str
    __data: CacheData

    def __init__(self, remote: str) -> None:
        self.__serial = -1
        self.__cache_dir = os.path.join(CONFIG_DIRNAME, "cache")
        self.__cache_file = os.path.join(self.__cache_dir, remote + ".json")
        self.__data = CacheData()

    @property
    def token(self) -> Token | None:
        self.__load()
        return self.__data.token

    @token.setter
    def token(self, token: Token) -> None:
        self.__load()
        self.__data.token = token
        self.__save()

    @token.deleter
    def token(self) -> None:
        if self.__data.token is not None:
            self.__clear()

    @property
    def user(self) -> User | None:
        return self.__data.user

    @user.setter
    def user(self, user: User) -> None:
        self.__load()
        self.__data.user = user
        self.__save()

    @user.deleter
    def user(self) -> None:
        if self.__data.user is not None:
            self.__clear()

    @property
    def laboratories(self) -> Laboratories:
        return self.__data.laboratories

    @laboratories.setter
    def laboratories(self, laboratories: Laboratories) -> None:
        self.__load()
        self.__data.laboratories = laboratories
        self.__save()

    def __clear(self) -> None:
        self.__data.clear()
        self.__save()

    def __load(self) -> None:
        if os.path.isfile(self.__cache_file):
            stat = os.stat(self.__cache_file)
            serial = hash((stat.st_uid, stat.st_gid, stat.st_mode, stat.st_size, stat.st_mtime))
            if self.__serial != serial:
                try:
                    with open(self.__cache_file) as f:
                        data = TypeAdapter(CacheData).validate_python(json.load(f))
                        if not data.verify_digest():
                            raise UnexpectedException("Cache data has been broken.")
                        self.__data = data
                except (ValidationError, UnexpectedException) as e:
                    self.__clear()
                    self.__save()
                    print(e)
                else:
                    self.__serial = serial
        else:
            self.__clear()
            self.__serial = -1

    def __save(self) -> None:
        self.__ensure_cache_dir()
        with open(self.__cache_file, "w") as f:
            FileLock.lock(f)
            self.__data.update_digest()
            f.write(json.dumps(dataclasses.asdict(self.__data)))
            FileLock.unlock(f)
        stat = os.stat(self.__cache_file)
        self.__serial = hash((stat.st_uid, stat.st_gid, stat.st_mode, stat.st_size, stat.st_mtime))
        # ensure file is secure.
        os.chmod(self.__cache_file, 0o600)

    def __ensure_cache_dir(self) -> None:
        if not os.path.exists(self.__cache_dir):
            os.makedirs(self.__cache_dir)
        # ensure directory is secure.
        os.chmod(self.__cache_dir, 0o700)
