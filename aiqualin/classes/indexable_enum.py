from enum import Enum
from typing import SupportsIndex

from typing_extensions import Self


class IndexableEnum(Enum):
    """A base class for creating indexable enumerations."""

    @classmethod
    def from_index(cls, index: SupportsIndex) -> Self:
        """Return the enumeration value corresponding to the given index.

        Args:
            index: The index of the enumeration value.

        Returns:
            The enumeration value corresponding to the given index.
        """
        return list(cls)[index]

    @classmethod
    def to_index(cls, value: Self) -> int:
        """Return the index of the given enumeration value.

        Args:
            value: The enumeration value.

        Returns:
            int: The index of the given enumeration value.
        """
        return list(cls).index(value)
