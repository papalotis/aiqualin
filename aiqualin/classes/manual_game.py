from dataclasses import dataclass, field

from rich import print

from aiqualin.classes.animal import Animal
from aiqualin.classes.cli_player import CLIPlayer, CLIPlayerWithBestMoveSuggestion
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
        default_factory=lambda: (
            CLIPlayerWithBestMoveSuggestion(Color),
            CLIPlayerWithBestMoveSuggestion(Animal),
        )
    )

    def play(self) -> None:
        while True:
            print("Who is starting? Color or Animal?")
            to_start = input('Enter "color" or "animal": ').strip().title()

            if to_start in ("Color", "Animal"):
                break
            else:
                print("Invalid input, please try again.")

        if (to_start == "Color" and self.players[0]._side == Animal) or (
            to_start == "Animal" and self.players[0]._side == Color
        ):
            self.players = (self.players[1], self.players[0])

        return super().play()

    def interpret_color_animal(
        self, color_or_animal: str, animal_or_color: str
    ) -> tuple[Color, Animal]:
        try:
            color_or_animal = Color(color_or_animal)
        except ValueError:
            color_or_animal, animal_or_color = animal_or_color, color_or_animal
            color_or_animal = Color(color_or_animal)
        animal_or_color = Animal(animal_or_color)
        return color_or_animal, animal_or_color

    def get_new_tile(self) -> Tile:
        """
        Prompts the user to enter the animal and color of a new tile and returns the corresponding Tile object.

        Returns:
            Tile: The new tile with the specified animal and color.
        """
        print()
        print("Enter the color and animal type of the new tile.")

        color_and_animal = tuple(input('Enter "color animal": ').strip().split())
        assert len(color_and_animal) == 2, "Invalid input"

        color, animal = self.interpret_color_animal(*color_and_animal)

        tile = Tile(animal=animal, color=color)
        assert tile != EMPTY_TILE

        return tile


if __name__ == "__main__":
    game = ManualGame()
    game.play()
