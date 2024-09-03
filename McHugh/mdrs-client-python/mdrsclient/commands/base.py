import re
from abc import ABC, abstractmethod
from typing import Any
from unicodedata import normalize

from mdrsclient.api import FoldersApi, LaboratoriesApi
from mdrsclient.config import ConfigFile
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import (
    IllegalArgumentException,
    MissingConfigurationException,
    UnauthorizedException,
    UnexpectedException,
)
from mdrsclient.models import Folder, Laboratory


class BaseCommand(ABC):
    @classmethod
    @abstractmethod
    def register(cls, parsers: Any) -> None:
        raise UnexpectedException("Not implemented.")

    @classmethod
    def _create_connection(cls, remote: str) -> MDRSConnection:
        config = ConfigFile(remote)
        if config.url is None:
            raise MissingConfigurationException(f"Remote host `{remote}` is not found.")
        return MDRSConnection(config.remote, config.url)

    @classmethod
    def _find_laboratory(cls, connection: MDRSConnection, name: str) -> Laboratory:
        if connection.laboratories.empty() or connection.token is not None and connection.token.is_expired:
            laboratory_api = LaboratoriesApi(connection)
            connection.laboratories = laboratory_api.list()
        laboratory = connection.laboratories.find_by_name(name)
        if laboratory is None:
            raise IllegalArgumentException(f"Laboratory `{name}` not found.")
        return laboratory

    @classmethod
    def _find_folder(
        cls, connection: MDRSConnection, laboratory: Laboratory, path: str, password: str | None = None
    ) -> Folder:
        folder_api = FoldersApi(connection)
        folders = folder_api.list(laboratory.id, normalize("NFC", path))
        if len(folders) != 1:
            raise UnexpectedException(f"Folder `{path}` not found.")
        if folders[0].lock:
            if password is None:
                raise UnauthorizedException(f"Folder `{path}` is locked.")
            folder_api.auth(folders[0].id, password)
        return folder_api.retrieve(folders[0].id)

    @classmethod
    def _parse_remote_host(cls, path: str) -> str:
        path_array = path.split(":")
        remote_host = path_array[0]
        if len(path_array) == 2 and path_array[1] != "" or len(path_array) > 2:
            raise IllegalArgumentException("Invalid remote host")
        return remote_host

    @classmethod
    def _parse_remote_host_with_path(cls, path: str) -> tuple[str, str, str]:
        path = re.sub(r"//+|/\./+|/\.$", "/", path)
        if re.search(r"/\.\./|/\.\.$", path) is not None:
            raise IllegalArgumentException("Path traversal found.")
        path_array = path.split(":")
        if len(path_array) != 2:
            raise IllegalArgumentException("Invalid remote host.")
        remote_host = path_array[0]
        folder_array = path_array[1].split("/")
        is_absolute_path = folder_array[0] == ""
        if not is_absolute_path:
            raise IllegalArgumentException("Must be absolute paths.")
        del folder_array[0]
        if len(folder_array) == 0:
            laboratory = ""
            folder = ""
        else:
            laboratory = folder_array.pop(0)
            folder = "/" + "/".join(folder_array)
        return (remote_host, laboratory, folder)
