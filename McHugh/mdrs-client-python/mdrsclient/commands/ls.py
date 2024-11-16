import json
from argparse import Namespace
from typing import Any

from pydantic.dataclasses import dataclass

from mdrsclient.api import FoldersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import UnauthorizedException
from mdrsclient.models import File, Folder, FolderSimple, Laboratory


class Config:
    arbitrary_types_allowed = True
    frozen = True


@dataclass(config=Config)
class LsCommandContext:
    prefix: str
    connection: MDRSConnection
    laboratory: Laboratory
    password: str
    is_json: bool
    is_quick: bool
    is_recursive: bool


class LsCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        ls_parser = parsers.add_parser("ls", help="list the folder contents")
        ls_parser.add_argument("-p", "--password", help="password to use when open locked folder")
        ls_parser.add_argument("-J", "--json", help="turn on json output", action="store_true")
        ls_parser.add_argument(
            "-q",
            "--quick",
            help="don't output header row. this option is forced if the -r option is specified",
            action="store_true",
        )
        ls_parser.add_argument("-r", "--recursive", help="list the folder contents recursive", action="store_true")
        ls_parser.add_argument("remote_path", help="remote folder path (remote:/lab/path/)")
        ls_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote_path = str(args.remote_path)
        password = str(args.password) if args.password else None
        is_json = bool(args.json)
        is_recursive = bool(args.recursive)
        is_quick = bool(args.quick) if not is_recursive else True
        cls.ls(remote_path, password, is_json, is_recursive, is_quick)

    @classmethod
    def ls(cls, remote_path: str, password: str | None, is_json: bool, is_recursive: bool, is_quick: bool) -> None:
        (remote, laboratory_name, r_path) = cls._parse_remote_host_with_path(remote_path)
        connection = cls._create_connection(remote)
        laboratory = cls._find_laboratory(connection, laboratory_name)
        context = LsCommandContext(
            f"{remote}:/{laboratory_name}",
            connection,
            laboratory,
            password if password is not None else "",
            is_json,
            is_quick,
            is_recursive,
        )
        folder = cls._find_folder(connection, laboratory, r_path, password)
        if context.is_json:
            cls._ls_json(context, folder)
        else:
            cls._ls_plain(context, folder)

    @classmethod
    def _ls_json(cls, context: LsCommandContext, folder: Folder) -> None:
        print(json.dumps(cls._folder2dict(context, folder), ensure_ascii=False))

    @classmethod
    def _ls_plain(cls, context: LsCommandContext, folder: Folder) -> None:
        label = {
            "type": "Type",
            "acl": "Access",
            "laboratory": "Laboratory",
            "size": "Size",
            "date": "Date",
            "name": "Name",
        }
        length: dict[str, int] = {}
        for key in label.keys():
            length[key] = len(label[key]) if not context.is_quick else 0
        for sub_folder in folder.sub_folders:
            sub_laboratory = context.connection.laboratories.find_by_id(sub_folder.laboratory_id)
            sub_laboratory_name = sub_laboratory.name if sub_laboratory is not None else "(invalid)"
            length["acl"] = max(length["acl"], len(sub_folder.access_level_name))
            length["laboratory"] = max(length["laboratory"], len(sub_laboratory_name))
            length["size"] = max(length["size"], len(str(folder.size)))
            length["date"] = max(length["date"], len(sub_folder.updated_at_name))
            length["name"] = max(length["name"], len(sub_folder.name))
        for file in folder.files:
            length["size"] = max(length["size"], len(str(file.size)))
            length["date"] = max(length["date"], len(file.updated_at_name))
            length["name"] = max(length["name"], len(file.name))
        length["acl"] = max(length["acl"], len(folder.access_level_name))
        length["laboratory"] = max(length["laboratory"], len(context.laboratory.name))
        header = (
            f"{label['type']:{length['type']}}\t{label['acl']:{length['acl']}}\t"
            f"{label['laboratory']:{length['laboratory']}}\t{label['size']:{length['size']}}\t"
            f"{label['date']:{length['date']}}\t{label['name']:{length['name']}}"
        )

        if context.is_recursive:
            print(f"{context.prefix}{folder.path}:")
            print(f"total {sum(f.size for f in folder.files)}")

        if not context.is_quick:
            print(header)
            print("-" * len(header.expandtabs()))

        for sub_folder in sorted(folder.sub_folders, key=lambda x: x.name):
            sub_laboratory_name = cls._laboratory_name(context, sub_folder.laboratory_id)
            sub_folder_type = "[d]" if sub_folder.lock is False else "[l]"
            print(
                f"{sub_folder_type:{length['type']}}\t{sub_folder.access_level_name:{length['acl']}}\t"
                f"{sub_laboratory_name:{length['laboratory']}}\t{sub_folder.size:{length['size']}}\t"
                f"{sub_folder.updated_at_name:{length['date']}}\t{sub_folder.name:{length['name']}}"
            )
        for file in sorted(folder.files, key=lambda x: x.name):
            print(
                f"{'[f]':{length['type']}}\t{folder.access_level_name:{length['acl']}}\t"
                f"{context.laboratory.name:{length['laboratory']}}\t{file.size:{length['size']}}\t"
                f"{file.updated_at_name:{length['date']}}\t{file.name:{length['name']}}"
            )

        if context.is_recursive:
            print("")
            for sub_folder in sorted(folder.sub_folders, key=lambda x: x.name):
                folder_api = FoldersApi(context.connection)
                try:
                    if sub_folder.lock:
                        folder_api.auth(sub_folder.id, context.password)
                    folder = folder_api.retrieve(sub_folder.id)
                    cls._ls_plain(context, folder)
                except UnauthorizedException:
                    pass

    @classmethod
    def _folder2dict(cls, context: LsCommandContext, folder: Folder | FolderSimple) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": folder.id,
            "pid": folder.pid,
            "name": folder.name,
            "size": folder.size,
            "access_level": folder.access_level_name,
            "lock": folder.lock,
            "laboratory": cls._laboratory_name(context, folder.laboratory_id),
            "description": folder.description,
            "created_at": folder.created_at,
            "updated_at": folder.updated_at,
        }
        if isinstance(folder, Folder):
            folder_api = FoldersApi(context.connection)
            data["metadata"] = folder_api.metadata(folder.id)
            if context.is_recursive:
                sub_folders: list[dict[str, Any]] = []
                for sub_folder in sorted(folder.sub_folders, key=lambda x: x.name):
                    try:
                        if sub_folder.lock:
                            folder_api.auth(sub_folder.id, context.password)
                        folder2 = folder_api.retrieve(sub_folder.id)
                        sub_folders.append(cls._folder2dict(context, folder2))
                    except UnauthorizedException:
                        pass
                data["sub_folders"] = sub_folders
            else:
                data["sub_folders"] = list(
                    map(lambda x: cls._folder2dict(context, x), sorted(folder.sub_folders, key=lambda x: x.name))
                )
            data["files"] = list(map(lambda x: cls._file2dict(context, x), sorted(folder.files, key=lambda x: x.name)))
        return data

    @classmethod
    def _file2dict(cls, context: LsCommandContext, file: File) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": file.id,
            "name": file.name,
            "type": file.type,
            "size": file.size,
            # "thumbnail": file.thumbnail,
            "description": file.description,
            "metadata": file.metadata,
            "download_url": f"{context.connection.url}/{file.download_url}",
            "created_at": file.created_at,
            "updated_at": file.updated_at,
        }
        return data

    @classmethod
    def _laboratory_name(cls, context: LsCommandContext, laboratory_id: int) -> str:
        laboratory = context.connection.laboratories.find_by_id(laboratory_id)
        return laboratory.name if laboratory is not None else "(invalid)"
