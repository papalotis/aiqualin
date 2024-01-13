from __future__ import annotations

from dataclasses import dataclass

from typing_extensions import Self

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
        *positions, placement_tile = string.split(",")

        (
            move_start_row,
            move_start_col,
            move_end_row,
            move_end_col,
            placement_row,
            placement_col,
        ) = map(int, positions)

        return cls(
            move_start_row=move_start_row,
            move_start_col=move_start_col,
            move_end_row=move_end_row,
            move_end_col=move_end_col,
            placement_row=placement_row,
            placement_col=placement_col,
            placement_tile=Tile.from_string(placement_tile),
        )
