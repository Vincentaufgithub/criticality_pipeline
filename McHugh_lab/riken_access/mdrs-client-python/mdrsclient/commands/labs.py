from argparse import Namespace
from typing import Any

from mdrsclient.api import LaboratoriesApi
from mdrsclient.commands.base import BaseCommand


class LabsCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        labs_parser = parsers.add_parser("labs", help="list all laboratories")
        labs_parser.add_argument("remote", help="label of remote host")
        labs_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote = str(args.remote)
        cls.labs(remote)

    @classmethod
    def labs(cls, remote: str) -> None:
        remote = cls._parse_remote_host(remote)
        connection = cls._create_connection(remote)
        laboratory_api = LaboratoriesApi(connection)
        laboratories = laboratory_api.list()
        connection.laboratories = laboratories
        label = {"id": "ID", "name": "Name", "pi_name": "PI", "full_name": "Laboratory"}
        length: dict[str, int] = {}
        for key in label.keys():
            length[key] = len(label[key])
        for laboratory in laboratories:
            length["id"] = max(length["id"], len(str(laboratory.id)))
            length["name"] = max(length["name"], len(laboratory.name))
            length["pi_name"] = max(length["pi_name"], len(laboratory.pi_name))
            length["full_name"] = max(length["full_name"], len(laboratory.full_name))
        header = (
            # f"{label['id']:{length['id']}}\t{label['name']:{length['name']}}\t"
            f"{label['name']:{length['name']}}\t"
            f"{label['pi_name']:{length['pi_name']}}\t{label['full_name']:{length['full_name']}}"
        )
        print(header)
        print("-" * len(header.expandtabs()))
        for laboratory in laboratories:
            print(
                # f"{laboratory.id:{length['id']}}\t{laboratory.name:{length['name']}}\t"
                f"{laboratory.name:{length['name']}}\t"
                f"{laboratory.pi_name:{length['pi_name']}}\t{laboratory.full_name:{length['full_name']}}"
            )
