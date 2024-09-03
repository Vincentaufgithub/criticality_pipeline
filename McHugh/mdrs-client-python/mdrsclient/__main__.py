import argparse
import sys

from mdrsclient.commands import (
    ChaclCommand,
    ConfigCommand,
    CpCommand,
    DownloadCommand,
    FileMetadataCommand,
    LabsCommand,
    LoginCommand,
    LogoutCommand,
    LsCommand,
    MetadataCommand,
    MkdirCommand,
    MvCommand,
    RmCommand,
    UploadCommand,
    WhoamiCommand,
)
from mdrsclient.exceptions import MDRSException


def main() -> None:
    description = """This is a command-line program for up- and downloading files to and from MDRS based repository."""

    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parsers = parser.add_subparsers(title="subcommands")

    ConfigCommand.register(parsers)
    LoginCommand.register(parsers)
    LogoutCommand.register(parsers)
    WhoamiCommand.register(parsers)
    LabsCommand.register(parsers)
    LsCommand.register(parsers)
    MkdirCommand.register(parsers)
    UploadCommand.register(parsers)
    DownloadCommand.register(parsers)
    MvCommand.register(parsers)
    CpCommand.register(parsers)
    RmCommand.register(parsers)
    ChaclCommand.register(parsers)
    MetadataCommand.register(parsers)
    FileMetadataCommand.register(parsers)

    try:
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()
    except MDRSException as e:
        print(f"Error: {e}")
        sys.exit(2)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
