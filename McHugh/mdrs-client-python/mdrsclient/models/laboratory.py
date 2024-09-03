from dataclasses import field
from typing import Generator

from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Laboratory:
    id: int
    name: str
    pi_name: str
    full_name: str


@dataclass(frozen=True)
class Laboratories:
    items: list[Laboratory] = field(default_factory=list)

    def __iter__(self) -> Generator[Laboratory, None, None]:
        yield from self.items

    def empty(self) -> bool:
        return len(self.items) == 0

    def clear(self) -> None:
        self.items.clear()

    def append(self, item: Laboratory) -> None:
        self.items.append(item)

    def sort(self) -> None:
        self.items.sort(key=lambda x: x.name)

    def find_by_id(self, id: int) -> Laboratory | None:
        return next((x for x in self.items if x.id == id), None)

    def find_by_name(self, name: str) -> Laboratory | None:
        return next((x for x in self.items if x.name == name), None)
