from typing import Any

from pydantic.dataclasses import dataclass

from mdrsclient.models.utils import iso8601_to_user_friendly


@dataclass(frozen=True)
class File:
    id: str
    name: str
    type: str
    size: int
    thumbnail: str | None
    description: str
    metadata: dict[str, Any]
    download_url: str
    created_at: str
    updated_at: str

    @property
    def created_at_name(self) -> str:
        return iso8601_to_user_friendly(self.created_at)

    @property
    def updated_at_name(self) -> str:
        return iso8601_to_user_friendly(self.updated_at)
