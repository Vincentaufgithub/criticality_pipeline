from typing import Any, Final, NamedTuple
from unicodedata import normalize

from pydantic.dataclasses import dataclass

from mdrsclient.models.file import File
from mdrsclient.models.utils import iso8601_to_user_friendly


class FolderAccessLevelItem(NamedTuple):
    mask: int
    key: str
    label: str


class FolderAccessLevel:
    # Bit Mask
    # - bit 0: Is Private
    # - bit 1: Is Public
    # - bit 2: With Password
    # - bit 3-7: (Reserved)
    # - bit 8-15: Restricted Open
    ACCESS_LEVELS: Final[list[FolderAccessLevelItem]] = [
        FolderAccessLevelItem(0x0204, "5kikan_or_pw_open", "5Kikan or PW Open"),
        FolderAccessLevelItem(0x0104, "cbs_or_pw_open", "CBS or PW Open"),
        FolderAccessLevelItem(0x0200, "5kikan_open", "5Kikan Open"),
        FolderAccessLevelItem(0x0100, "cbs_open", "CBS Open"),
        FolderAccessLevelItem(0x0004, "pw_open", "PW Open"),
        FolderAccessLevelItem(0x0002, "public", "Public"),
        FolderAccessLevelItem(0x0001, "private", "Private"),
        FolderAccessLevelItem(0x0000, "storage", "Storage"),
    ]

    @staticmethod
    def key2id(key: str) -> int | None:
        acl = next((x for x in FolderAccessLevel.ACCESS_LEVELS if x.key == key), None)
        return acl.mask if acl is not None else None

    @staticmethod
    def id2label(id: int) -> str | None:
        acl = next((x for x in FolderAccessLevel.ACCESS_LEVELS if (x.mask & id) == x.mask), None)
        return acl.label if acl is not None else None


@dataclass(frozen=True)
class FolderSimple:
    id: str
    pid: str | None
    name: str
    access_level: int
    lock: bool
    size: int
    laboratory_id: int
    description: str
    created_at: str
    updated_at: str
    restrict_opened_at: str | None

    @property
    def access_level_name(self) -> str:
        label = FolderAccessLevel.id2label(self.access_level)
        return label if label is not None else ""

    @property
    def lock_name(self) -> str:
        return "locked" if self.lock else "unlocked"

    @property
    def created_at_name(self) -> str:
        return iso8601_to_user_friendly(self.created_at)

    @property
    def updated_at_name(self) -> str:
        return iso8601_to_user_friendly(self.updated_at)


@dataclass(frozen=True)
class Folder(FolderSimple):
    metadata: list[dict[str, Any]]
    sub_folders: list[FolderSimple]
    files: list[File]
    path: str

    def find_sub_folder(self, name: str) -> FolderSimple | None:
        _name = normalize("NFC", name).lower()
        return next((x for x in self.sub_folders if x.name.lower() == _name), None)

    def find_file(self, name: str) -> File | None:
        _name = normalize("NFC", name).lower()
        return next((x for x in self.files if x.name.lower() == _name), None)
