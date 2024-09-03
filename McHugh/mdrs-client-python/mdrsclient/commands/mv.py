import os
from argparse import Namespace
from typing import Any
from unicodedata import normalize

from mdrsclient.api import FilesApi, FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.exceptions import IllegalArgumentException


class MvCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        mv_parser = parsers.add_parser("mv", help="move or rename the file or folder")
        mv_parser.add_argument("src_path", help="source remote path (remote:/lab/path/src)")
        mv_parser.add_argument("dest_path", help="destination remote path (remote:/lab/path/dest)")
        mv_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        src_path = str(args.src_path)
        dest_path = str(args.dest_path)
        cls.mv(src_path, dest_path)

    @classmethod
    def mv(cls, src_path: str, dest_path: str) -> None:
        (s_remote, s_laboratory_name, s_path) = cls._parse_remote_host_with_path(src_path)
        (d_remote, d_laboratory_name, d_path) = cls._parse_remote_host_with_path(dest_path)
        if s_remote != d_remote:
            raise IllegalArgumentException("Remote host mismatched.")
        if s_laboratory_name != d_laboratory_name:
            raise IllegalArgumentException("Laboratory mismatched.")
        s_path = s_path.rstrip("/")
        s_dirname = os.path.dirname(s_path)
        s_basename = os.path.basename(s_path)
        if d_path.endswith("/"):
            d_dirname = d_path
            d_basename = s_basename
        else:
            d_dirname = os.path.dirname(d_path)
            d_basename = os.path.basename(d_path)
        connection = cls._create_connection(s_remote)
        laboratory = cls._find_laboratory(connection, s_laboratory_name)
        s_parent_folder = cls._find_folder(connection, laboratory, s_dirname)
        d_parent_folder = cls._find_folder(connection, laboratory, d_dirname)
        s_file = s_parent_folder.find_file(s_basename)
        if s_file is not None:
            # source is file
            d_file = d_parent_folder.find_file(d_basename)
            if d_file is not None:
                raise IllegalArgumentException(f"File `{d_basename}` already exists.")
            d_sub_folder = d_parent_folder.find_sub_folder(d_basename)
            if d_sub_folder is not None:
                raise IllegalArgumentException(f"Cannot overwrite non-folder `{d_basename}` with folder `{d_path}`.")
            file_api = FilesApi(connection)
            if s_parent_folder.id != d_parent_folder.id or d_basename != s_basename:
                file_api.move(s_file, d_parent_folder.id, normalize("NFC", d_basename))
        else:
            s_folder = s_parent_folder.find_sub_folder(s_basename)
            if s_folder is None:
                raise IllegalArgumentException(f"File or folder `{s_basename}` not found.")
            # source is folder
            if d_parent_folder.find_file(d_basename) is not None:
                raise IllegalArgumentException(f"Cannot overwrite non-folder `{d_basename}` with folder `{s_path}`.")
            d_folder = d_parent_folder.find_sub_folder(d_basename)
            if d_folder is not None:
                if d_folder.id == s_folder.id:
                    raise IllegalArgumentException(f"`{s_path}` and `{s_path}` are the same folder.")
                raise IllegalArgumentException(f"Cannot move `{s_path}` to `{d_path}`: Folder not empty.")
            folder_api = FoldersApi(connection)
            if s_parent_folder.id != d_parent_folder.id or d_basename != s_basename:
                folder_api.move(s_folder, d_parent_folder.id, normalize("NFC", d_basename))
