from abc import ABC

import requests
from pydantic import TypeAdapter
from requests import Response

from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import (
    BadRequestException,
    ForbiddenException,
    UnauthorizedException,
    UnexpectedException,
)
from mdrsclient.models.error import DRFStandardizedErrors


class BaseApi(ABC):
    connection: MDRSConnection

    def __init__(self, connection: MDRSConnection) -> None:
        self.connection = connection

    def _raise_response_error(self, response: Response) -> None:
        if response.status_code >= 300:
            if response.status_code < 400 or response.status_code >= 500:
                raise UnexpectedException(f"Unexpected status code returned: {response.status_code}.")
            errors = TypeAdapter(DRFStandardizedErrors).validate_python(response.json())
            if response.status_code == requests.codes.bad_request:
                raise BadRequestException(errors.errors[0].detail)
            elif response.status_code == requests.codes.unauthorized:
                raise UnauthorizedException("Login required.")
            elif response.status_code == requests.codes.forbidden:
                raise ForbiddenException("You do not have enough permissions. Access is denied.")
            else:
                raise UnexpectedException(errors.errors[0].detail)
