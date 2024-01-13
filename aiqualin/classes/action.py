from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Self

from aiqualin.classes.animal import Animal
from aiqualin.classes.color import Color
from aiqualin.classes.tile import Tile


@dataclass(frozen=True, eq=True)
class Action:
    move_start_row: int
    move_start_col: int
    move_end_row: int
    move_end_col: int

    placement_row: int
    placement_col: int
    placement_tile: Tile

    @classmethod
    def from_string(cls, string: str) -> Self:
        *positions, animal_type, color_type = (
            string.split() if " " in string else string
        )

        if len(positions) not in (2, 6):
            raise ValueError("invalid action string")

        if len(positions) == 2:
            # this is a start action
            placement_row, placement_col = map(int, positions)
            move_start_row = move_start_col = move_end_row = move_end_col = -1
        elif len(positions) == 6:
            (
                move_start_row,
                move_start_col,
                move_end_row,
                move_end_col,
                placement_row,
                placement_col,
            ) = map(int, positions)
        else:
            raise ValueError("Unreachable")

        animal = Animal.from_index(int(animal_type))
        color = Color.from_index(int(color_type))

        return cls(
            move_start_row=move_start_row,
            move_start_col=move_start_col,
            move_end_row=move_end_row,
            move_end_col=move_end_col,
            placement_row=placement_row,
            placement_col=placement_col,
            placement_tile=Tile(animal=animal, color=color),
        )
