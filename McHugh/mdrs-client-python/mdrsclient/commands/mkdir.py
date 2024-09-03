import os
from argparse import Namespace
from typing import Any
from unicodedata import normalize

from mdrsclient.api import FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.exceptions import IllegalArgumentException


class MkdirCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        mkdir_parser = parsers.add_parser("mkdir", help="create a new folder")
        mkdir_parser.add_argument("remote_path", help="remote folder path (remote:/lab/path/)")
        mkdir_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        cls.mkdir(remote_path)

    @classmethod
    def mkdir(cls, remote_path: str) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        r_path = r_path.rstrip("/")
        r_dirname = os.path.dirname(r_path)
        r_basename = os.path.basename(r_path)
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        parent_folder = cls._find_folder(connection, laboratory, r_dirname)
        if parent_folder.find_sub_folder(r_basename) is not None or parent_folder.find_file(r_basename) is not None:
            raise IllegalArgumentException(f"Cannot create folder `{r_path}`: File exists.")
        folder_api = FoldersApi(connection)
        folder_api.create(normalize("NFC", r_basename), parent_folder.id)
