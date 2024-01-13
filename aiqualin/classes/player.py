from abc import ABC, abstractmethod

from aiqualin.classes.action import Action
from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.game_scorer import GameScorer
from aiqualin.classes.tile import Tile


class AbstractPlayer(ABC):
    def __init__(self, side: type[Animal | Color]) -> None:
        self._side = side

    @property
    def our_side(self) -> type[Animal | Color]:
        return self._side

    @property
    def their_side(self) -> type[Animal | Color]:
        return Animal if self.our_side == Color else Color

    def our_score(self, board: Board) -> int:
        return GameScorer(board).score_for_property(self.our_side)

    def their_score(self, board: Board) -> int:
        return GameScorer(board).score_for_property(self.their_side)

    @abstractmethod
    def next_action(
        self, board: Board, open_tiles: list[Tile], closed_tiles: list[Tile]
    ) -> Action:
        raise NotImplementedError
