import mimetypes
import os
from typing import Any, Final

from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass
from requests_toolbelt.multipart.encoder import MultipartEncoder

from mdrsclient.api.base import BaseApi
from mdrsclient.api.utils import token_check
from mdrsclient.exceptions import UnexpectedException
from mdrsclient.models import File


@dataclass(frozen=True)
class FilesApiCreateResponse:
    id: str


class FilesApi(BaseApi):
    ENTRYPOINT: Final[str] = "v3/files/"
    FALLBACK_MIMETYPE: Final[str] = "application/octet-stream"

    def retrieve(self, id: str) -> File:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + id + "/"
        token_check(self.connection)
        response = self.connection.get(url)
        self._raise_response_error(response)
        return TypeAdapter(File).validate_python(response.json())

    def create(self, folder_id: str, path: str) -> str:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT
        token_check(self.connection)
        data: dict[str, str | int] | MultipartEncoder = {}
        try:
            with open(os.path.realpath(path), mode="rb") as fp:
                data = MultipartEncoder(
                    fields={"folder_id": folder_id, "file": (os.path.basename(path), fp, self._get_mime_type(path))}
                )
                response = self.connection.post(url, data=data, headers={"Content-Type": data.content_type})
                self._raise_response_error(response)
                ret = TypeAdapter(FilesApiCreateResponse).validate_python(response.json())
        except OSError:
            raise UnexpectedException(f"Could not open `{path}` file.")
        except MemoryError:
            raise UnexpectedException("Out of memory.")
        except Exception as e:
            raise UnexpectedException("Unspecified error.") from e
        return ret.id

    def update(self, file: File, path: str | None) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + file.id + "/"
        token_check(self.connection)
        data: dict[str, str | int] | MultipartEncoder = {}
        if path is not None:
            # update file body
            try:
                with open(os.path.realpath(path), mode="rb") as fp:
                    data = MultipartEncoder(fields={"file": (os.path.basename(path), fp, self._get_mime_type(path))})
                    response = self.connection.put(url, data=data, headers={"Content-Type": data.content_type})
            except OSError:
                raise UnexpectedException(f"Could not open `{path}` file.")
            except MemoryError:
                raise UnexpectedException("Out of memory.")
            except Exception as e:
                raise UnexpectedException("Unspecified error.") from e
        else:
            # update metadata
            data = {"name": file.name, "description": file.description}
            response = self.connection.put(url, data=data)
        self._raise_response_error(response)
        return True

    def destroy(self, file: File) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + file.id + "/"
        token_check(self.connection)
        response = self.connection.delete(url)
        self._raise_response_error(response)
        return True

    def move(self, file: File, folder_id: str, name: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + file.id + "/move/"
        data: dict[str, str | int] = {"folder": folder_id, "name": name}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        return True

    def copy(self, file: File, folder_id: str, name: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + file.id + "/copy/"
        data: dict[str, str | int] = {"folder": folder_id, "name": name}
        token_check(self.connection)
        response = self.connection.post(url, data=data)
        self._raise_response_error(response)
        return True

    def metadata(self, file: File) -> dict[str, Any]:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = self.ENTRYPOINT + file.id + "/metadata/"
        token_check(self.connection)
        response = self.connection.get(url)
        self._raise_response_error(response)
        return response.json()

    def download(self, file: File, path: str) -> bool:
        # print(self.__class__.__name__ + "::" + sys._getframe().f_code.co_name)
        url = file.download_url
        token_check(self.connection)
        response = self.connection.get(url, stream=True)
        self._raise_response_error(response)
        try:
            with open(path, "wb") as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        except PermissionError:
            print(f"Cannot create file `{path}`: Permission denied.")
        return True

    def _get_mime_type(self, path: str) -> str:
        mt = mimetypes.guess_type(path)
        if mt:
            return mt[0] or self.FALLBACK_MIMETYPE
        return self.FALLBACK_MIMETYPE
