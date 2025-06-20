from dataclasses import dataclass
from pydantic import BaseModel
from typing import TypeVar, Generic


T = TypeVar('T', bound=BaseModel)


@dataclass
class ResponseValidationResult(Generic[T]):
    data: T | None
    errors: list[str]

    def is_valid(self) -> bool:
        return not self.errors
