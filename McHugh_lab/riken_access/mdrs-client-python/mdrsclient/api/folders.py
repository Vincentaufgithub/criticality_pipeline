from typing import Any, Final

import requests
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from mdrsclient.api.base import BaseApi
from mdrsclient.api.utils import token_check
from mdrsclient.exceptions import UnauthorizedException
from mdrsclient.models import Folder, FolderSimple


@dataclass(frozen=True)
class FoldersApiCreateResponse:
    id: str


class FoldersApi(BaseApi):
    ENTRYPOINT: Final[str] = "v3/folders/"

    def list(self, laboratory_id: int, path: str) -> list[FolderSimple]:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT
        params: dict[str, str | int] = {"path": path, "laboratory_id": laboratory_id}
        token_check(self.connection)
        response = self.connection.get(url, params=params)
        self._raise_response_error(response)
        ret: list[FolderSimple] = []
        for data in response.json():
            ret.append(TypeAdapter(FolderSimple).validate_python(data))
        return ret

    def retrieve(self, id: str) -> Folder:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/"
        token_check(self.connection)
        response = self.connection.get(url)
        self._raise_response_error(response)
        ret = TypeAdapter(Folder).validate_python(response.json())
        return ret

    def create(self, name: str, parent_id: str) -> str:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT
        data: dict[str, str | int] = {"name": name, "parent_id": parent_id, "description": "", "template_id": -1}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        ret = TypeAdapter(FoldersApiCreateResponse).validate_python(response.json())
        return ret.id

    def update(self, folder: FolderSimple) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + folder.id + "/"
        data: dict[str, str | int] = {
            "name": folder.name,
            "description": folder.description,
        }
        token_check(self.connection)
        response = self.connection.put(url, data=data)
        self._raise_response_error(response)
        return True

    def destroy(self, id: str, recursive: bool) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/"
        params: dict[str, str | int] = {"recursive": str(recursive)}
        token_check(self.connection)
        response = self.connection.delete(url, params=params)
        self._raise_response_error(response)
        return True

    def auth(self, id: str, password: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/auth/"
        data: dict[str, str | int] = {"password": password}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        if response.status_code == requests.codes.unauthorized:
            raise UnauthorizedException("Password is incorrect.")
        self._raise_response_error(response)
        return True

    def acl(self, id: str, access_level: int, recursive: bool, password: str | None) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/acl/"
        data: dict[str, str | int] = {"access_level": access_level}
        if password is not None:
            data.update({"password": password})
        if recursive is True:
            data.update({"lower": 1})
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        return True

    def move(self, folder: FolderSimple, folder_id: str, name: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + folder.id + "/move/"
        data: dict[str, str | int] = {"parent": folder_id, "name": name}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        return True

    def copy(self, folder: FolderSimple, folder_id: str, name: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + folder.id + "/copy/"
        data: dict[str, str | int] = {"parent": folder_id, "name": name}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        return True

    def metadata(self, id: str) -> dict[str, Any]:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/metadata/"
        token_check(self.connection)
        response = self.connection.get(url)
        self._raise_response_error(response)
        return response.json()
