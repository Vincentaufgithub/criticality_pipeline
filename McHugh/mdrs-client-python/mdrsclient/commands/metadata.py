import json
from argparse import Namespace
from typing import Any

from mdrsclient.api import FoldersApi
from mdrsclient.commands.base import BaseCommand


class MetadataCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        metadata_parser = parsers.add_parser("metadata", help="get a folder metadata")
        metadata_parser.add_argument("-p", "--password", help="password to use when open locked folder")
        metadata_parser.add_argument("remote_path", help="remote folder path (remote:/lab/path/)")
        metadata_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        password = str(args.password) if args.password else None
        cls.metadata(remote_path, password)

    @classmethod
    def metadata(cls, remote_path: str, password: str | None) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        folder = cls._find_folder(connection, laboratory, r_path, password)
        folder_api = FoldersApi(connection)
        metadata = folder_api.metadata(folder.id)
        print(json.dumps(metadata, ensure_ascii=False))
