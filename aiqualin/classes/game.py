from dataclasses import dataclass, field
from typing import Any

from aiqualin.classes.action import Action
from aiqualin.classes.action_generator import ActionGenerator
from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.tile import Tile


def create_full_closed_tiles() -> list[Tile]:
    tiles = []
    for animal in Animal:
        if animal == Animal.EMPTY:
            continue

        for color in Color:
            if color == Color.EMPTY:
                continue

            tiles.append(Tile(animal=animal, color=color))
    return tiles


N_OPEN_TILES = 6


@dataclass
class Game:
    board: Board = field(default_factory=Board.empty_board)
    open_tiles: list[Tile] = field(default_factory=list)
    closed_tiles: list[Tile] = field(default_factory=create_full_closed_tiles)

    def __post_init__(self) -> None:
        self.replenish_open_tiles()

    def replenish_open_tiles(self) -> None:
        while len(self.open_tiles) < N_OPEN_TILES and len(self.closed_tiles) > 0:
            self.open_tiles.append(self.closed_tiles.pop())

    def play_action(self, action: Action) -> None:
        self.board = self.board.apply_action(action)

        # remove currently placed tile from open tiles
        self.open_tiles.remove(action.placement_tile)

        self.replenish_open_tiles()

    def play_cli(self) -> None:
        while True:
            print(len(self.open_tiles))
            print(len(self.closed_tiles))

            self.board.visualize()

            actions = list(
                ActionGenerator(
                    self.board, self.open_tiles, self.closed_tiles
                ).generate_actions()
            )

            new_boards = [self.board.apply_action(action) for action in actions]

            # print("Possible actions:")
            # for i, action in enumerate(actions):
            #     print(f"{i}: {action}")

            action_str = input("Enter action index: ")
            if action_str == "q":
                break

            action_index = int(action_str)

            action = list(actions)[action_index]

            self.play_action(action)
            print()


if __name__ == "__main__":
    Game().play_cli()
