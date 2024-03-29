import random
from dataclasses import dataclass, field

from rich import print

from aiqualin.classes.action import Action
from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.cli_player import CLIPlayer
from aiqualin.classes.color import Color
from aiqualin.classes.game_scorer import GameScorer
from aiqualin.classes.player import AbstractPlayer
from aiqualin.classes.simple_score_based_ai import SimpleScoreBasedAI
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
    players: tuple[AbstractPlayer, AbstractPlayer] = field(
        default_factory=lambda: (SimpleScoreBasedAI(Color), SimpleScoreBasedAI(Animal))
    )
    player_names: tuple[str, str] = field(init=False)

    def __post_init__(self) -> None:
        self.shuffle_closed_tiles()

        self.replenish_open_tiles()

        player_names = tuple(player.__class__.__name__ for player in self.players)
        if player_names[0] == player_names[1]:
            player_names = tuple(
                f"{player_name}_{i}"
                for i, player_name in enumerate(player_names, start=1)
            )

        self.player_names = player_names

    def shuffle_closed_tiles(self) -> None:
        random.shuffle(self.closed_tiles)

    def replenish_open_tiles(self) -> None:
        while len(self.open_tiles) < N_OPEN_TILES and len(self.closed_tiles) > 0:
            n_need_to_replenish = N_OPEN_TILES - len(self.open_tiles)
            print(f"Need to replenish {n_need_to_replenish} more tiles.")
            try:
                new_tile = self.get_new_tile()
            except Exception:
                print("\n[red]Error:[/red] Invalid input, try again!")

                continue
            try:
                index_in_closed_tiles = self.closed_tiles.index(new_tile)
            except ValueError:
                # tile is not in closed tiles
                print("\n[red]Error:[/red] Tile is not in closed tiles, try again!")
            else:
                self.open_tiles.append(self.closed_tiles.pop(index_in_closed_tiles))

    def get_new_tile(self) -> Tile:
        return self.closed_tiles[0]

    def play_action(self, action: Action) -> None:
        self.board = self.board.apply_action(action)

        # remove currently placed tile from open tiles
        self.open_tiles.remove(action.placement_tile)

        self.replenish_open_tiles()

    def play(self) -> None:
        while len(self.open_tiles) > 0:
            for i, player in enumerate(self.players):
                player_name = self.player_names[i]
                print(f"{player_name}'s turn:")

                action = player.next_action(
                    self.board, self.open_tiles, self.closed_tiles
                )
                # print("Action:", action)
                self.play_action(action)
                print()
                self.board.visualize()
                print()
                print(
                    f"Animal score: {GameScorer(self.board).score_for_property(Animal)}"
                )
                print(
                    f"Color score: {GameScorer(self.board).score_for_property(Color)}"
                )
                print()

        score_animals = GameScorer(self.board).score_for_property(Animal)
        score_colors = GameScorer(self.board).score_for_property(Color)

        print("Final score:")
        print(f"  Animals: {score_animals}")
        print(f"  Colors: {score_colors}")

        if score_animals > score_colors:
            print("Animals win!")
        elif score_animals < score_colors:
            print("Colors win!")
        else:
            print("Tie!")


if __name__ == "__main__":
    Game().play()
