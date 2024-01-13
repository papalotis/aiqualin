from enum import Enum

from typing_extensions import Self


class IndexableEnum(Enum):
    @classmethod
    def from_index(cls, index) -> Self:
        return list(cls)[index]

    @classmethod
    def to_index(cls, value) -> int:
        return list(cls).index(value)
