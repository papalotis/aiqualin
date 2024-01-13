from dataclasses import dataclass

from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.tile import EMPTY_TILE, Tile


@dataclass
class GameScorer:
    """
    This is the scoring method that I use with Frau Kaya(r). In the real game, Ls are considered contiguous, but when we play we only consider horizontal or vertical groupings.
    """

    board: Board

    def get_property_from_tile(
        self, tile: Tile, property_to_score: type[Animal | Color]
    ) -> Animal | Color:
        if property_to_score == Animal:
            return tile.animal
        elif property_to_score == Color:
            return tile.color

        raise ValueError("property_to_score must be Animal or Color")

    def n_lengths_for_sequence(
        self, sequence: list[Tile], property_to_score: type[Animal | Color]
    ) -> dict[int, int]:
        lengths_appearances = {i: 0 for i in range(1, 7)}

        # find the lengths of consecutive tiles with the same property
        current_length = 1
        for i in range(len(sequence)):
            current_tile = sequence[i]

            if i == len(sequence) - 1:
                next_tile = EMPTY_TILE
            else:
                next_tile = sequence[i + 1]

            current_property = self.get_property_from_tile(
                current_tile, property_to_score
            )
            next_property = self.get_property_from_tile(next_tile, property_to_score)

            if current_property == next_property and next_tile != EMPTY_TILE:
                current_length += 1
            else:
                lengths_appearances[current_length] += 1
                current_length = 1

        return lengths_appearances

    def n_lengths_horizontal(
        self, property_to_score: type[Animal | Color]
    ) -> dict[int, int]:
        lengths_appearances = {i: 0 for i in range(1, 7)}

        for row in self.board.tiles:
            lengths_appearances_in_row = self.n_lengths_for_sequence(
                row, property_to_score
            )
            for length, appearances in lengths_appearances_in_row.items():
                lengths_appearances[length] += appearances

        return lengths_appearances

    def n_lengths_vertical(
        self, property_to_score: type[Animal | Color]
    ) -> dict[int, int]:
        lengths_appearances = {i: 0 for i in range(1, 7)}

        for col in range(len(self.board.tiles[0])):
            column = [row[col] for row in self.board.tiles]
            lengths_appearances_in_column = self.n_lengths_for_sequence(
                column, property_to_score
            )
            for length, appearances in lengths_appearances_in_column.items():
                lengths_appearances[length] += appearances

        return lengths_appearances

    def n_lengths(self, property_to_score: type[Animal | Color]) -> dict[int, int]:
        n_lengths_horizontal = self.n_lengths_horizontal(property_to_score)
        n_lengths_vertical = self.n_lengths_vertical(property_to_score)

        lengths_appearances = {
            k: n_lengths_horizontal[k] + n_lengths_vertical[k]
            for k in n_lengths_horizontal.keys()
        }

        return lengths_appearances

    def score_for_property(self, property_to_score: type[Animal | Color]) -> int:
        lengths_appearances = self.n_lengths(property_to_score)

        length_to_score_map = {
            1: 0,
            2: 1,
            3: 3,
            4: 6,
            5: 10,
            6: 15,
        }

        score = sum(
            length_to_score_map[length] * appearances
            for length, appearances in lengths_appearances.items()
        )

        return score

    @property
    def score(self) -> int:
        score_animal = self.score_for_property(Animal)
        score_color = self.score_for_property(Color)

        # the difference between the two scores is the final score
        return score_animal - score_color
