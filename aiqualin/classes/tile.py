from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Self

from aiqualin.classes.animal import Animal
from aiqualin.classes.color import Color


@dataclass(frozen=True)
class Tile:
    animal: Animal
    color: Color

    def __post_init__(self) -> None:
        animal_is_empty = self.animal == Animal.EMPTY
        color_is_empty = self.color == Color.EMPTY
        # either both are empty or both are not empty
        assert (
            animal_is_empty == color_is_empty
        ), "animal and color must be both empty or both not empty"

    def short_string(self) -> str:
        if self == EMPTY_TILE:
            return "EMPTY"

        animal_index = Animal.to_index(self.animal)
        color_index = Color.to_index(self.color)

        return f"({animal_index},{color_index})"

    @classmethod
    def from_short_string(cls, string: str) -> Self:
        if string == "EMPTY":
            return EMPTY_TILE

        string = (
            string.replace("(", "")
            .replace(")", "")
            .replace("{", "")
            .replace("}", "")
            .replace("[", "")
            .replace("]", "")
        )
        animal_index, color_index = map(int, string.split(","))

        animal = Animal.from_index(animal_index)
        color = Color.from_index(color_index)

        return cls(animal=animal, color=color)

    def pretty_string(self) -> str:
        if self == EMPTY_TILE:
            return "EMPTY"

        animal_name = self.animal.value
        color_name = self.color.value

        return f"{animal_name.title()} {color_name.title()}"


EMPTY_TILE = Tile(animal=Animal.EMPTY, color=Color.EMPTY)

__all__ = ["Tile", "EMPTY_TILE"]
