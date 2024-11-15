from argparse import Namespace
from typing import Any

from mdrsclient.api import FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.exceptions import IllegalArgumentException
from mdrsclient.models import FolderAccessLevel


class ChaclCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        chacl_parser = parsers.add_parser("chacl", help="change the folder access level")
        chacl_parser.add_argument("access_level", help="access level (private, cbs_open, pw_open)")
        chacl_parser.add_argument("-r", "--recursive", help="change access levels recursively", action="store_true")
        chacl_parser.add_argument("-p", "--password", help="password to set when access level is `pw_open`")
        chacl_parser.add_argument("remote_path", help="remote folder path (remote:/lab/path/)")
        chacl_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        access_level = FolderAccessLevel.key2id(str(args.access_level))
        if access_level is None:
            raise IllegalArgumentException(
                "Invalid `access_level` parameter. must be `private`, `cbs_open` or `pw_open`."
            )
        password = str(args.password) if args.password else None
        is_recursive = bool(args.recursive)
        cls.chacl(remote_path, access_level, is_recursive, password)

    @classmethod
    def chacl(cls, remote_path: str, access_level: int, is_recursive: bool, password: str | None) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        r_path = r_path.rstrip("/")
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        folder = cls._find_folder(connection, laboratory, r_path)
        folder_api = FoldersApi(connection)
        folder_api.acl(folder.id, access_level, is_recursive, password)
