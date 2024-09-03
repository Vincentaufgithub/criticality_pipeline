import os
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pydantic.dataclasses import dataclass

from mdrsclient.api import FilesApi, FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import IllegalArgumentException, MDRSException
from mdrsclient.models import Folder
from mdrsclient.settings import CONCURRENT


@dataclass(frozen=True)
class UploadFileInfo:
    folder: Folder
    path: str


class UploadCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        upload_parser = parsers.add_parser("upload", help="upload the file or directory")
        upload_parser.add_argument(
            "-r", "--recursive", help="upload directories and their contents recursive", action="store_true"
        )
        upload_parser.add_argument(
            "-s",
            "--skip-if-exists",
            help="skip the upload if file is already uploaded and file size is the same",
            action="store_true",
        )
        upload_parser.add_argument("local_path", help="local file path (/foo/bar/data.txt)")
        upload_parser.add_argument("remote_path", help="remote folder path (remote:/lab/path/)")
        upload_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        local_path = str(args.local_path)
        remote_path = str(args.remote_path)
        is_recursive = bool(args.recursive)
        is_skip_if_exists = bool(args.skip_if_exists)
        cls.upload(local_path, remote_path, is_recursive, is_skip_if_exists)

    @classmethod
    def upload(cls, local_path: str, remote_path: str, is_recursive: bool, is_skip_if_exists: bool) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        l_path = os.path.abspath(local_path)
        if not os.path.exists(l_path):
            raise IllegalArgumentException(f"File or directory `{local_path}` not found.")
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        folder = cls._find_folder(connection, laboratory, r_path)
        infos: list[UploadFileInfo] = []
        if os.path.isdir(l_path):
            if not is_recursive:
                raise IllegalArgumentException(f"Cannot upload `{local_path}`: Is a directory.")
            folder_api = FoldersApi(connection)
            folder_map: dict[str, Folder] = {}
            folder_map[r_path] = folder
            l_basename = os.path.basename(l_path)
            for dirpath, _, filenames in os.walk(l_path, followlinks=True):
                sub = l_basename if dirpath == l_path else os.path.join(l_basename, os.path.relpath(dirpath, l_path))
                d_dirname = os.path.join(r_path, sub)
                d_basename = os.path.basename(d_dirname)
                # prepare destination parent path
                d_parent_dirname = os.path.dirname(d_dirname)
                if folder_map.get(d_parent_dirname) is None:
                    folder_map[d_parent_dirname] = cls._find_folder(connection, laboratory, d_parent_dirname)
                # prepare destination path
                if folder_map.get(d_dirname) is None:
                    d_folder = folder_map[d_parent_dirname].find_sub_folder(d_basename)
                    if d_folder is None:
                        d_folder_id = folder_api.create(d_basename, folder_map[d_parent_dirname].id)
                    else:
                        d_folder_id = d_folder.id
                    print(d_dirname)
                    folder_map[d_dirname] = folder_api.retrieve(d_folder_id)
                    if d_folder is None:
                        folder_map[d_parent_dirname].sub_folders.append(folder_map[d_dirname])
                # register upload file list
                for filename in filenames:
                    infos.append(UploadFileInfo(folder_map[d_dirname], os.path.join(dirpath, filename)))
        else:
            infos.append(UploadFileInfo(folder, l_path))
        cls.__multiple_upload(connection, infos, is_skip_if_exists)

    @classmethod
    def __multiple_upload(
        cls, connection: MDRSConnection, infos: list[UploadFileInfo], is_skip_if_exists: bool
    ) -> None:
        file_api = FilesApi(connection)
        with ThreadPoolExecutor(max_workers=CONCURRENT) as pool:
            pool.map(lambda x: cls.__multiple_upload_worker(file_api, x, is_skip_if_exists), infos)

    @classmethod
    def __multiple_upload_worker(cls, file_api: FilesApi, info: UploadFileInfo, is_skip_if_exists: bool) -> None:
        basename = os.path.basename(info.path)
        file = info.folder.find_file(basename)
        try:
            if file is None:
                file_api.create(info.folder.id, info.path)
            elif not is_skip_if_exists or file.size != os.path.getsize(info.path):
                file_api.update(file, info.path)
            print(os.path.join(info.folder.path, basename))
        except MDRSException as e:
            print(f"Error: {e}")
