import os
from argparse import Namespace
from typing import Any

from mdrsclient.api import FilesApi, FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.exceptions import IllegalArgumentException


class RmCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        rm_parser = parsers.add_parser("rm", help="remove the file or folder")
        rm_parser.add_argument(
            "-r", "--recursive", help="remove folders and their contents recursive", action="store_true"
        )
        rm_parser.add_argument("remote_path", help="remote file path (remote:/lab/path/file)")
        rm_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        is_recursive = bool(args.recursive)
        cls.rm(remote_path, is_recursive)

    @classmethod
    def rm(cls, remote_path: str, is_recursive: bool) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        r_path = r_path.rstrip("/")
        r_dirname = os.path.dirname(r_path)
        r_basename = os.path.basename(r_path)
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        parent_folder = cls._find_folder(connection, laboratory, r_dirname)
        file = parent_folder.find_file(r_basename)
        if file is not None:
            file_api = FilesApi(connection)
            file_api.destroy(file)
        else:
            folder = parent_folder.find_sub_folder(r_basename)
            if folder is None:
                raise IllegalArgumentException(f"Cannot remove `{r_path}`: No such file or folder.")
            if not is_recursive:
                raise IllegalArgumentException(f"Cannot remove `{r_path}`: Is a folder.")
            folder_api = FoldersApi(connection)
            folder_api.destroy(folder.id, True)
