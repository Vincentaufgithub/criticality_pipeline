from typing import Final

from pydantic import TypeAdapter

from mdrsclient.api.base import BaseApi
from mdrsclient.api.utils import token_check
from mdrsclient.models import Laboratories, Laboratory


class LaboratoriesApi(BaseApi):
    ENTRYPOINT: Final[str] = "v3/laboratories/"

    def list(self) -> Laboratories:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT
        token_check(self.connection)
        response = self.connection.get(url)
        self._raise_response_error(response)
        ret = Laboratories()
        for data in response.json():
            ret.append(TypeAdapter(Laboratory).validate_python(data))
        ret.sort()
        return ret
