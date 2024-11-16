from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class DRFStandardizedError:
    code: str
    detail: str
    attr: str | None


@dataclass(frozen=True)
class DRFStandardizedErrors:
    type: str
    errors: list[DRFStandardizedError]
