import os
from typing import IO, Any

if os.name == "nt":
    import msvcrt
elif os.name == "posix":
    import fcntl


class FileLock:
    @staticmethod
    def lock(file: IO[Any]) -> None:
        if os.name == "nt":
            msvcrt.locking(file.fileno(), msvcrt.LK_LOCK, 1)
        elif os.name == "posix":
            fcntl.flock(file.fileno(), fcntl.LOCK_EX)

    @staticmethod
    def unlock(file: IO[Any]) -> None:
        if os.name == "nt":
            msvcrt.locking(file.fileno(), msvcrt.LK_UNLCK, 1)
        elif os.name == "posix":
            fcntl.flock(file.fileno(), fcntl.LOCK_UN)
