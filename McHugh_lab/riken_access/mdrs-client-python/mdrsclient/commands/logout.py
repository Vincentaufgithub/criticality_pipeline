from argparse import Namespace
from typing import Any

from mdrsclient.commands.base import BaseCommand
from mdrsclient.config import ConfigFile
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import MissingConfigurationException


class LogoutCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        logout_parser = parsers.add_parser("logout", help="logout from remote host")
        logout_parser.add_argument("remote", help="label of remote host")
        logout_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote = str(args.remote)
        cls.logout(remote)

    @classmethod
    def logout(cls, remote: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is None:
            raise MissingConfigurationException(f"Remote host `{remote}` is not found.")
        connection = MDRSConnection(config.remote, config.url)
        connection.logout()
