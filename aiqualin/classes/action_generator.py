from collections.abc import Iterable
from dataclasses import dataclass

from aiqualin.classes.action import Action
from aiqualin.classes.board import Board
from aiqualin.classes.tile import EMPTY_TILE, Tile


@dataclass
class ActionGenerator:
    board: Board
    open_tiles: list[Tile]
    closed_tiles: list[Tile]

    def all_positions(self) -> set[tuple[int, int]]:
        return_value = set()

        for row_index in range(len(self.board.tiles)):
            for col_index in range(len(self.board.tiles[row_index])):
                return_value.add((row_index, col_index))

        return return_value

    def positions_of_empty_tiles(self) -> Iterable[tuple[int, int]]:
        for row_index, row in enumerate(self.board.tiles):
            for col_index, tile in enumerate(row):
                if tile == EMPTY_TILE:
                    yield row_index, col_index

    def positions_of_non_empty_tiles(self) -> Iterable[tuple[int, int]]:
        for row_index, row in enumerate(self.board.tiles):
            for col_index, tile in enumerate(row):
                if tile != EMPTY_TILE:
                    yield row_index, col_index

    def generate_actions_for_position_in_direction(
        self, col: int, row: int, d_col: int, d_row: int
    ) -> set[Action]:
        actions: set[Action] = set()

        assert (d_col, d_row) in [(1, 0), (-1, 0), (0, 1), (0, -1)], (d_col, d_row)

        empty_positions = set(self.positions_of_empty_tiles())

        if (row, col) in empty_positions:
            # trying to find out what happens if we move an empty tile
            # this is not allowed
            return actions

        for new_tile in self.open_tiles:
            move_tile_col = col
            move_tile_row = row
            # this is the special version I play with Frau Kaya(r)
            # where tiles can move only one step and moving is mandatory
            # set to inf to play the original game
            n_iterations_allowed = 1
            i = 0
            while i < n_iterations_allowed:
                i += 1
                move_tile_col += d_col
                move_tile_row += d_row

                if self.board.last_action is not None:
                    if (
                        move_tile_col == self.board.last_action.move_start_col
                        and move_tile_row == self.board.last_action.move_start_row
                        and col == self.board.last_action.move_end_col
                        and row == self.board.last_action.move_end_row
                    ):
                        # we would be undoing the move part of the
                        # last move, so we are not allowed to do this
                        continue

                if move_tile_col not in range(len(self.board.tiles)):
                    break

                if move_tile_row not in range(len(self.board.tiles[move_tile_col])):
                    break

                tile_at_move_position = self.board.tiles[move_tile_row][move_tile_col]
                if tile_at_move_position != EMPTY_TILE:
                    # we found a blocking tile
                    break

                empty_tiles_for_move = (
                    empty_positions - {(move_tile_row, move_tile_col)}
                ) | {(row, col)}
                for empty_tile_y, empty_tile_x in empty_tiles_for_move:
                    new_action = Action(
                        move_start_row=row,
                        move_start_col=col,
                        move_end_row=move_tile_row,
                        move_end_col=move_tile_col,
                        placement_row=empty_tile_y,
                        placement_col=empty_tile_x,
                        placement_tile=new_tile,
                    )
                    actions.add(new_action)

        return actions

    def generate_actions_for_position(self, col: int, row: int) -> set[Action]:
        actions: set[Action] = set()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_actions = self.generate_actions_for_position_in_direction(
                col=col, row=row, d_col=dx, d_row=dy
            )
            actions |= new_actions

        return actions

    def generate_start_actions(self) -> set[Action]:
        actions: set[Action] = set()
        for row, col in self.positions_of_empty_tiles():
            for tile in self.open_tiles:
                new_move = Action(
                    move_start_row=-1,
                    move_start_col=-1,
                    move_end_row=-1,
                    move_end_col=-1,
                    placement_row=row,
                    placement_col=col,
                    placement_tile=tile,
                )
                actions.add(new_move)

        return actions

    def generate_actions(self) -> set[Action]:
        if self.board.last_action is None and self.board.is_empty():
            return self.generate_start_actions()

        moves: set[Action] = set()
        for row, col in self.positions_of_non_empty_tiles():
            moves |= self.generate_actions_for_position(col=col, row=row)

        return moves
