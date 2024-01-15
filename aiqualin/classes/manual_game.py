from dataclasses import dataclass, field

from rich import print

from aiqualin.classes.animal import Animal
from aiqualin.classes.cli_player import CLIPlayer
from aiqualin.classes.color import Color
from aiqualin.classes.game import Game
from aiqualin.classes.player import AbstractPlayer
from aiqualin.classes.tile import EMPTY_TILE, Tile



@dataclass
class ManualGame(Game):
    """
    Represents a manual game where the players are prompted to enter their moves through the command line interface.
    """

    players: tuple[AbstractPlayer, AbstractPlayer] = field(
        default_factory=lambda: (CLIPlayer(Color), CLIPlayer(Animal))
    )

    def get_new_tile(self) -> Tile:
        """
        Prompts the user to enter the animal and color of a new tile and returns the corresponding Tile object.

        Returns:
            Tile: The new tile with the specified animal and color.
        """
        print()
        print("What animal is the new tile?")
        for animal in Animal:
            if animal == Animal.EMPTY:
                continue

            print(f"{Animal.to_index(animal)+1}: {animal.name}")

        index_animal = int(input("Enter the index of the animal: ")) - 1

        print("What color is the new tile?")
        for color in Color:
            if color == Color.EMPTY:
                continue

            print(f"[{color.name.lower()}]{Color.to_index(color)+1}: {color.name}")

        index_color = int(input("Enter the index of the color: ")) - 1

        tile = Tile(
            animal=Animal.from_index(index_animal), color=Color.from_index(index_color)
        )
        assert tile != EMPTY_TILE

        return tile


if __name__ == "__main__":
    game = ManualGame()
    game.play()
