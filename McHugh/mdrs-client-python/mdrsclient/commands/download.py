import os
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from pydantic.dataclasses import dataclass

from mdrsclient.api import FilesApi, FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import IllegalArgumentException, UnexpectedException
from mdrsclient.models import File, Folder, Laboratory
from mdrsclient.settings import CONCURRENT


@dataclass(frozen=True)
class DownloadFileInfo:
    file: File
    path: str


@dataclass
class DownloadContext:
    hasError: bool
    files: list[DownloadFileInfo]


class DownloadCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        download_parser = parsers.add_parser("download", help="download the file or folder")
        download_parser.add_argument(
            "-r", "--recursive", help="download folders and their contents recursive", action="store_true"
        )
        download_parser.add_argument(
            "-e", "--exclude", help="exclude to download path matched file or folders", action="append"
        )
        download_parser.add_argument("-p", "--password", help="password to use when open locked folder")
        download_parser.add_argument("remote_path", help="remote file path (remote:/lab/path/file)")
        download_parser.add_argument("local_path", help="local folder path (/foo/bar/)")
        download_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        local_path = str(args.local_path)
        is_recursive = bool(args.recursive)
        password = str(args.password) if args.password else None
        excludes = list(map(lambda x: str(x).rstrip("/").lower(), args.exclude)) if args.exclude is not None else []
        cls.download(remote_path, local_path, is_recursive, password, excludes)

    @classmethod
    def download(
        cls, remote_path: str, local_path: str, is_recursive: bool, password: str | None, excludes: list[str]
    ) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        r_path = r_path.rstrip("/")
        r_dirname = os.path.dirname(r_path)
        r_basename = os.path.basename(r_path)
        connection = cls._create_connection(remote)
        l_dirname = os.path.realpath(local_path)
        if not os.path.isdir(l_dirname):
            raise IllegalArgumentException(f"Local directory `{local_path}` not found.")
        laboratory = cls._find_laboratory(connection, laboratory_name)
        r_parent_folder = cls._find_folder(connection, laboratory, r_dirname, password)
        file = r_parent_folder.find_file(r_basename)
        if file is not None:
            if cls.__check_excludes(excludes, laboratory, r_parent_folder, file):
                return
            context = DownloadContext(False, [])
            l_path = os.path.join(l_dirname, r_basename)
            context.files.append(DownloadFileInfo(file, l_path))
            cls.__multiple_download(connection, context)
        else:
            folder = r_parent_folder.find_sub_folder(r_basename)
            if folder is None:
                raise IllegalArgumentException(f"File or folder `{r_path}` not found.")
            if not is_recursive:
                raise IllegalArgumentException(f"Cannot download `{r_path}`: Is a folder.")
            folder_api = FoldersApi(connection)
            cls.__multiple_download_pickup_recursive_files(
                connection, folder_api, laboratory, folder.id, l_dirname, excludes
            )

    @classmethod
    def __multiple_download_pickup_recursive_files(
        cls,
        connection: MDRSConnection,
        folder_api: FoldersApi,
        laboratory: Laboratory,
        folder_id: str,
        basedir: str,
        excludes: list[str],
    ) -> None:
        context = DownloadContext(False, [])
        folder = folder_api.retrieve(folder_id)
        dirname = os.path.join(basedir, folder.name)
        if cls.__check_excludes(excludes, laboratory, folder, None):
            return
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        print(dirname)
        for file in folder.files:
            if cls.__check_excludes(excludes, laboratory, folder, file):
                continue
            path = os.path.join(dirname, file.name)
            context.files.append(DownloadFileInfo(file, path))
        cls.__multiple_download(connection, context)
        if context.hasError:
            raise UnexpectedException("Some files failed to download.")
        for sub_folder in folder.sub_folders:
            cls.__multiple_download_pickup_recursive_files(
                connection, folder_api, laboratory, sub_folder.id, dirname, excludes
            )

    @classmethod
    def __multiple_download(cls, connection: MDRSConnection, context: DownloadContext) -> None:
        file_api = FilesApi(connection)
        with ThreadPoolExecutor(max_workers=CONCURRENT) as pool:
            results = pool.map(lambda x: cls.__multiple_download_worker(file_api, x), context.files)
            hasError = next(filter(lambda x: x is False, results), None)
            if hasError is not None:
                context.hasError = True

    @classmethod
    def __multiple_download_worker(cls, file_api: FilesApi, info: DownloadFileInfo) -> bool:
        try:
            file_api.download(info.file, info.path)
        except Exception:
            return False
        print(info.path)
        return True

    @classmethod
    def __check_excludes(cls, excludes: list[str], laboratory: Laboratory, folder: Folder, file: File | None) -> bool:
        path = f"/{laboratory.name}{folder.path}{file.name if file is not None else ''}".rstrip("/").lower()
        return path in excludes
