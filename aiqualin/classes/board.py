from __future__ import annotations

import copy
from dataclasses import dataclass

from rich import print
from typing_extensions import Self

from aiqualin.classes.action import Action
from aiqualin.classes.animal import Animal
from aiqualin.classes.color import Color
from aiqualin.classes.tile import EMPTY_TILE, Tile


@dataclass(frozen=True)
class Board:
    tiles: list[list[Tile]]

    def apply_action(self, action: Action) -> Board:
        tiles = copy.deepcopy(self.tiles)

        move_coordinates = (
            action.move_start_row,
            action.move_start_col,
            action.move_end_row,
            action.move_end_col,
        )

        if all(coordinate == -1 for coordinate in move_coordinates):
            # this is an action without movement
            pass
        elif -1 in move_coordinates:
            raise ValueError("cannot have partial move")
        else:
            # make sure that the tile at the start is not empty
            tile_at_start = tiles[action.move_start_row][action.move_start_col]
            assert tile_at_start != EMPTY_TILE, "cannot move from empty tile"

            # make start tile empty
            tiles[action.move_start_row][action.move_start_col] = EMPTY_TILE
            # move tile to end
            tiles[action.move_end_row][action.move_end_col] = tile_at_start

        # place tile
        try:
            tile_at_placement = tiles[action.placement_row][action.placement_col]
            assert (
                tile_at_placement == EMPTY_TILE
            ), "cannot place tile on non-empty tile"
            tiles[action.placement_row][action.placement_col] = action.placement_tile
        except AssertionError:
            print()
            self.visualize()
            print()
            print(action)
            print()
            raise

        return Board(tiles=tiles)

    @classmethod
    def empty_board(cls) -> Self:
        n_grid = 6
        tiles = [
            [Tile(animal=Animal.EMPTY, color=Color.EMPTY) for _ in range(n_grid)]
            for _ in range(n_grid)
        ]

        board = cls(tiles=tiles)

        return board

    def visualize(self) -> None:
        rows = []
        for row in self.tiles:
            tiles_to_print = []
            for tile in row:
                short_string = tile.short_string()

                tiles_to_print.append(short_string)

            rows += [" ".join(tiles_to_print)]

        # rows += ["\n"]
        print("\n".join(rows))

    @classmethod
    def from_pretty_string(cls, pretty_string: str) -> Self:
        rows = pretty_string.splitlines()
        tiles = []

        for row in rows:
            tiles.append([])
            row = row.strip()
            for tile_string in row.split(" "):
                tile = Tile.from_short_string(tile_string)
                tiles[-1].append(tile)

        return cls(tiles=tiles)

    def is_empty(self) -> bool:
        return all(tile == EMPTY_TILE for row in self.tiles for tile in row)
