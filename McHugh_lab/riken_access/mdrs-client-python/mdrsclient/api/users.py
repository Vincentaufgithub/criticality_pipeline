from typing import Final

import requests
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from mdrsclient.api.base import BaseApi
from mdrsclient.exceptions import UnauthorizedException
from mdrsclient.models import Token, User


@dataclass(frozen=True)
class UsersCurrentResponseLaboratory:
    id: int
    name: str
    role: int


@dataclass(frozen=True)
class UsersApiCurrentResponse:
    id: int
    username: str
    full_name: str
    email: str
    laboratories: list[UsersCurrentResponseLaboratory]
    is_staff: bool
    is_active: bool
    is_superuser: bool
    is_reviewer: bool
    last_login: str  # ISO8601
    date_joined: str  # ISO8601


class UsersApi(BaseApi):
    ENTRYPOINT: Final[str] = "v3/users/"

    def current(self) -> User:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + "current/"
        response = self.connection.get(url)
        self._raise_response_error(response)
        obj = TypeAdapter(UsersApiCurrentResponse).validate_python(response.json())
        laboratory_ids = list(map(lambda x: x.id, obj.laboratories))
        user = User(id=obj.id, username=obj.username, laboratory_ids=laboratory_ids, is_reviewer=obj.is_reviewer)
        return user

    def token(self, username: str, password: str) -> Token:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + "token/"
        data: dict[str, str | int] = {"username": username, "password": password}
        response = self.connection.post(url, data=data)
        if response.status_code == requests.codes.unauthorized:
            raise UnauthorizedException("Invalid username or password.")
        self._raise_response_error(response)
        token = TypeAdapter(Token).validate_python(response.json())
        return token

    def tokenRefresh(self, token: Token) -> Token:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + "token/refresh/"
        data: dict[str, str | int] = {"refresh": token.refresh}
        response = self.connection.post(url, data=data)
        if response.status_code == requests.codes.unauthorized:
            raise UnauthorizedException("Token is invalid or expired.")
        self._raise_response_error(response)
        token = TypeAdapter(Token).validate_python(response.json())
        return token
