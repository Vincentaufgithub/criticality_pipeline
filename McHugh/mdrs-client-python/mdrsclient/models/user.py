import time

import jwt
from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class DecodedJWT:
    token_type: str
    exp: int
    iat: int
    jti: str
    user_id: int


@dataclass(frozen=True)
class Token:
    access: str
    refresh: str

    @property
    def user_id(self) -> int:
        access_decoded = self.__decode(self.access)
        return access_decoded.user_id

    @property
    def is_expired(self) -> bool:
        now = int(time.time())
        refresh_decoded = self.__decode(self.refresh)
        return (now - 10) > refresh_decoded.exp

    @property
    def is_refresh_required(self) -> bool:
        now = int(time.time())
        access_decoded = self.__decode(self.access)
        refresh_decoded = self.__decode(self.refresh)
        return (now + 10) > access_decoded.exp and (now - 10) < refresh_decoded.exp

    def __decode(self, token: str) -> DecodedJWT:
        data = jwt.decode(token, options={"verify_signature": False})  # type: ignore
        return TypeAdapter(DecodedJWT).validate_python(data)


@dataclass(frozen=True)
class User:
    id: int
    username: str
    laboratory_ids: list[int]
    is_reviewer: bool
