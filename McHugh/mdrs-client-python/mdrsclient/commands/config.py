from argparse import Namespace
from typing import Any, Callable

from mdrsclient.commands.base import BaseCommand
from mdrsclient.config import ConfigFile
from mdrsclient.exceptions import IllegalArgumentException


class ConfigCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        # config
        config_parser = parsers.add_parser("config", help="configure remote hosts")
        func_help: Callable[[Namespace], None] = lambda _: config_parser.print_help()
        config_parser.set_defaults(func=func_help)
        config_parsers = config_parser.add_subparsers(title="config subcommands")
        # config create
        create_parser = config_parsers.add_parser("create", help="create a new remote host")
        create_parser.add_argument("remote", help="label of remote host")
        create_parser.add_argument("url", help="API entrypoint url of remote host")
        create_parser.set_defaults(func=cls.func_create)
        # config update
        update_parser = config_parsers.add_parser("update", help="update a new remote host")
        update_parser.add_argument("remote", help="label of remote host")
        update_parser.add_argument("url", help="API entrypoint url of remote host")
        update_parser.set_defaults(func=cls.func_update)
        # config list
        list_parser = config_parsers.add_parser("list", help="list all the remote hosts", aliases=["ls"])
        list_parser.add_argument("-l", "--long", help="show the api url", action="store_true")
        list_parser.set_defaults(func=cls.func_list)
        # config delete
        delete_parser = config_parsers.add_parser("delete", help="delete an existing remote host", aliases=["remove"])
        delete_parser.add_argument("remote", help="label of remote host")
        delete_parser.set_defaults(func=cls.func_delete)

    @classmethod
    def func_create(cls, args: Namespace) -> None:
        remote = str(args.remote)
        url = str(args.url)
        cls.create(remote, url)

    @classmethod
    def func_update(cls, args: Namespace) -> None:
        remote = str(args.remote)
        url = str(args.url)
        cls.update(remote, url)

    @classmethod
    def func_list(cls, args: Namespace) -> None:
        is_long = bool(args.long)
        cls.list(is_long)

    @classmethod
    def func_delete(cls, args: Namespace) -> None:
        remote = str(args.remote)
        cls.delete(remote)

    @classmethod
    def create(cls, remote: str, url: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is not None:
            raise IllegalArgumentException(f"Remote host `{remote}` is already exists.")
        else:
            config.url = url

    @classmethod
    def update(cls, remote: str, url: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is None:
            raise IllegalArgumentException(f"Remote host `{remote}` is not exists.")
        else:
            config.url = url

    @classmethod
    def list(cls, is_long: bool) -> None:
        config = ConfigFile("")
        for remote, url in config.list():
            line = f"{remote}:"
            if is_long:
                line += f"\t{url}"
            print(line)

    @classmethod
    def delete(cls, remote: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is None:
            raise IllegalArgumentException(f"Remote host `{remote}` is not exists.")
        else:
            del config.url
