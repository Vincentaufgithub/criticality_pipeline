import configparser
import os
from typing import Final

import validators  # type: ignore

from mdrsclient.exceptions import IllegalArgumentException
from mdrsclient.settings import CONFIG_DIRNAME
from mdrsclient.utils import FileLock


class ConfigFile:
    OPTION_URL: Final[str] = "url"
    CONFIG_FILENAME: Final[str] = "config.ini"
    remote: str
    __serial: int
    __config_dirname: str
    __config_path: str
    __config: configparser.ConfigParser

    def __init__(self, remote: str) -> None:
        self.remote = remote
        self.__serial = -1
        self.__config_dirname = CONFIG_DIRNAME
        self.__config_path = os.path.join(CONFIG_DIRNAME, self.CONFIG_FILENAME)
        self.__config = configparser.ConfigParser()

    def list(self) -> list[tuple[str, str]]:
        ret: list[tuple[str, str]] = []
        self.__load()
        for remote in self.__config.sections():
            url = self.__config.get(remote, self.OPTION_URL)
            ret.append((remote, url))
        return ret

    @property
    def url(self) -> str | None:
        if not self.__exists(self.remote):
            return None
        return self.__config.get(self.remote, self.OPTION_URL)

    @url.setter
    def url(self, url: str) -> None:
        if not validators.url(url):  # type: ignore
            raise IllegalArgumentException("malformed URI sequence")
        self.__load()
        if self.__config.has_section(self.remote):
            self.__config.remove_section(self.remote)
        self.__config.add_section(self.remote)
        self.__config.set(self.remote, self.OPTION_URL, url)
        self.__save()

    @url.deleter
    def url(self) -> None:
        if self.__exists(self.remote):
            self.__config.remove_section(self.remote)
            self.__save()

    def __exists(self, section: str) -> bool:
        self.__load()
        return self.__config.has_option(section, self.OPTION_URL)

    def __load(self) -> None:
        if os.path.isfile(self.__config_path):
            stat = os.stat(self.__config_path)
            serial = hash(stat)
            if self.__serial != serial:
                self.__config.read(self.__config_path, encoding="utf8")
                self.__serial = serial

    def __save(self) -> None:
        self.__ensure_cache_dir()
        with open(self.__config_path, "w") as f:
            FileLock.lock(f)
            self.__config.write(f)
            FileLock.unlock(f)
        os.chmod(self.__config_path, 0o600)

    def __ensure_cache_dir(self) -> None:
        if not os.path.exists(self.__config_dirname):
            os.makedirs(self.__config_dirname)
        # ensure directory is secure.
        os.chmod(self.__config_dirname, 0o700)
