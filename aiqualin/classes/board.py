from __future__ import annotations

import copy
from dataclasses import dataclass

from typing_extensions import Self

from aiqualin.classes.action import Action
from aiqualin.classes.animal import Animal
from aiqualin.classes.color import Color
from aiqualin.classes.tile import EMPTY_TILE, Tile


@dataclass(frozen=True)
class Board:
    tiles: list[list[Tile]]
    last_action: Action | None

    def apply_action(self, action: Action) -> Board:
        # make sure that the movement of this action
        # does not undo the movement of the last action
        if self.last_action is not None:
            if (
                action.move_start_row == self.last_action.move_end_row
                and action.move_start_col == self.last_action.move_end_col
                and action.move_end_row == self.last_action.move_start_row
                and action.move_end_col == self.last_action.move_start_col
            ):
                self.visualize()
                print()
                print(action)
                print()
                print(self.last_action)
                raise ValueError("cannot undo last move")

        tiles = copy.deepcopy(self.tiles)

        no_move_in_action = (
            action.move_start_col == -1
            and action.move_start_row == -1
            and action.move_end_col == -1
            and action.move_end_row == -1
        )

        if no_move_in_action:
            n_non_empty_tiles = sum(tile != EMPTY_TILE for row in tiles for tile in row)
            assert n_non_empty_tiles == 0

        if not no_move_in_action:
            # make sure that the tile at the start is not empty
            tile_at_start = tiles[action.move_start_row][action.move_start_col]
            assert tile_at_start != EMPTY_TILE, "cannot move from empty tile"

            # make start tile empty
            tiles[action.move_start_row][action.move_start_col] = EMPTY_TILE
            # move tile to end
            tiles[action.move_end_row][action.move_end_col] = tile_at_start

        # place tile
        tile_at_placement = tiles[action.placement_row][action.placement_col]
        assert tile_at_placement == EMPTY_TILE, "cannot place tile on non-empty tile"
        tiles[action.placement_row][action.placement_col] = action.placement_tile

        return Board(tiles=tiles, last_action=action)

    @classmethod
    def empty_board(cls) -> Self:
        n_grid = 6
        tiles = [
            [Tile(animal=Animal.EMPTY, color=Color.EMPTY) for _ in range(n_grid)]
            for _ in range(n_grid)
        ]

        board = cls(tiles=tiles, last_action=None)

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
    def from_pretty_string(cls, pretty_string: str, last_action: Action | None) -> Self:
        rows = pretty_string.splitlines()
        tiles = []
        for row in rows:
            tiles.append([])
            row = row.strip()
            for tile_string in row.split(" "):
                tile = Tile.from_short_string(tile_string)
                tiles[-1].append(tile)

        return Board(tiles=tiles, last_action=last_action)

    def is_empty(self) -> bool:
        return all(tile == EMPTY_TILE for row in self.tiles for tile in row)
