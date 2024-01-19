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
        self, col: int, row: int, d_col: int, d_row: int, add_no_movement_action: bool
    ) -> set[Action]:
        actions: set[Action] = set()

        assert (d_col, d_row) in [(1, 0), (-1, 0), (0, 1), (0, -1)], (d_col, d_row)

        empty_positions = set(self.positions_of_empty_tiles())

        if (row, col) in empty_positions:
            # trying to find out what happens if we move an empty tile
            # this is not allowed
            raise ValueError("Trying to move an empty tile")

        move_tile_col = col
        move_tile_row = row
        n_iterations_allowed = 10
        i = 0
        while i < n_iterations_allowed:
            if i > 0:
                move_tile_col += d_col
                move_tile_row += d_row
            i += 1

            # moved out of the board
            if move_tile_col not in range(len(self.board.tiles)):
                break

            # moved out of the board
            if move_tile_row not in range(len(self.board.tiles[move_tile_col])):
                break

            tile_at_move_position = self.board.tiles[move_tile_row][move_tile_col]
            if tile_at_move_position != EMPTY_TILE:
                if (move_tile_row, move_tile_col) == (
                    row,
                    col,
                ):
                    if add_no_movement_action:
                        # this is the case where we are not moving a tile
                        move_kwargs = dict(
                            move_start_row=-1,
                            move_start_col=-1,
                            move_end_row=-1,
                            move_end_col=-1,
                        )
                        # since we do not move the tile, we can place it exactly
                        # where the empty tiles are currently
                        empty_tiles_for_placement = set(empty_positions)
                    else:
                        continue

                else:
                    # we found a tile in the way, we can't move further
                    break
            else:
                # we want to both move a tile and place a tile
                move_kwargs = dict(
                    move_start_row=row,
                    move_start_col=col,
                    move_end_row=move_tile_row,
                    move_end_col=move_tile_col,
                )
                # remove the tile that has currently been moved to
                # from the potential empty tiles and add the tile that
                # we are moving from to the empty tiles
                empty_tiles_for_placement = (
                    empty_positions - {(move_tile_row, move_tile_col)}
                ) | {(row, col)}

            for empty_tile_y, empty_tile_x in empty_tiles_for_placement:
                for new_tile in self.open_tiles:
                    new_action = Action(
                        **move_kwargs,
                        placement_row=empty_tile_y,
                        placement_col=empty_tile_x,
                        placement_tile=new_tile,
                    )
                    actions.add(new_action)

        return actions

    def generate_actions_for_position(self, col: int, row: int) -> set[Action]:
        actions: set[Action] = set()

        for i, (d_col, d_row) in enumerate([(1, 0), (-1, 0), (0, 1), (0, -1)]):
            add_no_movement_action = i == 0
            new_actions = self.generate_actions_for_position_in_direction(
                col=col,
                row=row,
                d_col=d_col,
                d_row=d_row,
                add_no_movement_action=add_no_movement_action,
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
        if self.board.is_empty():
            return self.generate_start_actions()

        moves: set[Action] = set()
        for row, col in self.positions_of_non_empty_tiles():
            moves |= self.generate_actions_for_position(col=col, row=row)

        return moves
