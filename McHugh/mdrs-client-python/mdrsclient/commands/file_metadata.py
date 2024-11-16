import json
import os
from argparse import Namespace
from typing import Any

from mdrsclient.api import FilesApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.exceptions import IllegalArgumentException


class FileMetadataCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        file_metadata_parser = parsers.add_parser("file-metadata", help="get the file metadata")
        file_metadata_parser.add_argument("-p", "--password", help="password to use when open locked folder")
        file_metadata_parser.add_argument("remote_path", help="remote file path (remote:/lab/path/file)")
        file_metadata_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        password = str(args.password) if args.password else None
        cls.file_metadata(remote_path, password)

    @classmethod
    def file_metadata(cls, remote_path: str, password: str | None) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        r_path = r_path.rstrip("/")
        r_dirname = os.path.dirname(r_path)
        r_basename = os.path.basename(r_path)
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        folder = cls._find_folder(connection, laboratory, r_dirname, password)
        file = folder.find_file(r_basename)
        if file is None:
            raise IllegalArgumentException(f"File `{r_basename}` not found.")
        file_api = FilesApi(connection)
        metadata = file_api.metadata(file)
        print(json.dumps(metadata, ensure_ascii=False))
