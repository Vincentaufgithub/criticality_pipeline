from mdrsclient.api.users import UsersApi
from mdrsclient.connection import MDRSConnection
from mdrsclient.exceptions import UnauthorizedException


def token_check(connection: MDRSConnection) -> None:
    try:
        connection.lock.acquire()
        if connection.token is not None:
            if connection.token.is_refresh_required:
                user_api = UsersApi(connection)
                try:
                    connection.token = user_api.tokenRefresh(connection.token)
                except UnauthorizedException:
                    connection.logout()
            elif connection.token.is_expired:
                connection.logout()
    finally:
        connection.lock.release()
