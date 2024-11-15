import getpass
from argparse import Namespace
from typing import Any

from mdrsclient.api import UsersApi
from mdrsclient.commands.base import BaseCommand
from mdrsclient.config import ConfigFile
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import MissingConfigurationException


class LoginCommand(BaseCommand):
    @classmethod
    def register(cls, parsers: Any) -> None:
        login_parser = parsers.add_parser("login", help="login to remote host")
        login_parser.add_argument("-u", "--username", help="login username")
        login_parser.add_argument("-p", "--password", help="login password")
        login_parser.add_argument("remote", help="label of remote host")
        login_parser.set_defaults(func=cls.func)

    @classmethod
    def func(cls, args: Namespace) -> None:
        remote = str(args.remote)
        username = str(args.username) if args.password else input("Username: ").strip()
        password = str(args.password) if args.password else getpass.getpass("Password: ").strip()
        cls.login(remote, username, password)

    @classmethod
    def login(cls, remote: str, username: str, password: str) -> None:
        remote = cls._parse_remote_host(remote)
        config = ConfigFile(remote)
        if config.url is None:
            raise MissingConfigurationException(f"Remote host `{remote}` is not found.")
        connection = MDRSConnection(config.remote, config.url)
        user_api = UsersApi(connection)
        token = user_api.token(username, password)
        connection.token = token
        user = user_api.current()
        connection.user = user
        print("Login Successful")
