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

        for i in range(len(self.board.tiles)):
            for j in range(len(self.board.tiles[i])):
                return_value.add((i, j))

        return return_value

    def positions_of_empty_tiles(self) -> Iterable[tuple[int, int]]:
        for i, row in enumerate(self.board.tiles):
            for j, tile in enumerate(row):
                if tile == EMPTY_TILE:
                    yield i, j

    def positions_of_non_empty_tiles(self) -> Iterable[tuple[int, int]]:
        for i, row in enumerate(self.board.tiles):
            for j, tile in enumerate(row):
                if tile != EMPTY_TILE:
                    yield i, j

    def generate_actions_for_position_in_direction(
        self, x: int, y: int, dx: int, dy: int
    ) -> set[Action]:
        actions: set[Action] = set()

        move_tile_x = x
        move_tile_y = y

        empty_positions = set(self.positions_of_empty_tiles())

        for new_tile in self.open_tiles:
            # this is the special version I play with Frau Kaya(r)
            # where tiles can move only one step
            # set to inf to play the original game
            n_iterations_allowed = 1
            i = 0
            while i < n_iterations_allowed:
                i += 1
                move_tile_x += dx
                move_tile_y += dy

                if self.board.last_action is not None:
                    if (
                        move_tile_x == self.board.last_action.move_start_col
                        and move_tile_y == self.board.last_action.move_start_row
                    ):
                        print("skipping position where ")
                        # we would be undoing the move part of the
                        # last move, so we are not allowed to do this
                        continue

                if move_tile_x not in range(len(self.board.tiles)):
                    break

                if move_tile_y not in range(len(self.board.tiles[move_tile_x])):
                    break

                tile_at_move_position = self.board.tiles[move_tile_x][move_tile_y]
                if tile_at_move_position != EMPTY_TILE:
                    # we found a blocking tile
                    break

                empty_tiles_for_move = (empty_positions - {(x, y)}) | {
                    (move_tile_x, move_tile_y)
                }
                for empty_tile_x, empty_tile_y in empty_tiles_for_move:
                    new_action = Action(
                        move_start_row=x,
                        move_start_col=y,
                        move_end_row=move_tile_x,
                        move_end_col=move_tile_y,
                        placement_row=empty_tile_x,
                        placement_col=empty_tile_y,
                        placement_tile=new_tile,
                    )
                    actions.add(new_action)

        return actions

    def generate_actions_for_position(self, x: int, y: int) -> set[Action]:
        actions: set[Action] = set()
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_actions = self.generate_actions_for_position_in_direction(
                x=x, y=y, dx=dx, dy=dy
            )
            actions |= new_actions

        return actions

    def generate_start_actions(self) -> set[Action]:
        actions: set[Action] = set()
        for x, y in self.positions_of_empty_tiles():
            for tile in self.open_tiles:
                new_move = Action(
                    move_start_row=-1,
                    move_start_col=-1,
                    move_end_row=-1,
                    move_end_col=-1,
                    placement_row=x,
                    placement_col=y,
                    placement_tile=tile,
                )
                actions.add(new_move)

        return actions

    def generate_actions(self) -> set[Action]:
        if self.board.last_action is None and self.board.is_empty():
            return self.generate_start_actions()

        moves: set[Action] = set()
        for x, y in self.positions_of_non_empty_tiles():
            moves |= self.generate_actions_for_position(x=x, y=y)

        return moves
