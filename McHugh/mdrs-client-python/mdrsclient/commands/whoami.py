from argparse import Namespace
from typing import Any, Final

from mdrsclient.commands.base import BaseCommand
from mdrsclient.config import ConfigFile
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import MissingConfigurationException


class WhoamiCommand(BaseCommand):
    ANONYMOUS_USERNAME: Final[str] = "(Anonymous)"

    @classmethod
    def register(cls, parsers: Any) -> None:
        whoami_parser = parsers.add_parser("whoami", help="show current user name")
        whoami_parser.add_argument("remote", help="label of remote host")
        whoami_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote = str(args.remote)
        cls.whoami(remote)

    @classmethod
    def whoami(cls, remote: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is None:
            raise MissingConfigurationException(f"Remote host `{remote}` is not found.")
        connection = MDRSConnection(config.remote, config.url)
        if connection.token is not None and connection.token.is_expired:
            connection.logout()
        username = connection.user.username if connection.user is not None else cls.ANONYMOUS_USERNAME
        print(username)
