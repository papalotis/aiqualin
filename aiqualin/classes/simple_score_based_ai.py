from aiqualin.classes.action import Action
from aiqualin.classes.action_generator import ActionGenerator
from aiqualin.classes.board import Board
from aiqualin.classes.player import AbstractPlayer
from aiqualin.classes.tile import Tile


class SimpleScoreBasedAI(AbstractPlayer):
    def score_board(self, board: Board) -> int:
        our_score = self.our_score(board)
        their_score = self.their_score(board)

        return our_score - their_score

    def next_action(
        self, board: Board, open_tiles: list[Tile], closed_tiles: list[Tile]
    ) -> Action:
        next_actions = list(
            ActionGenerator(board, open_tiles, closed_tiles).generate_actions()
        )

        next_boards = (board.apply_action(action) for action in next_actions)

        next_scores = [self.score_board(next_board) for next_board in next_boards]

        index_best_score = next_scores.index(max(next_scores))

        return next_actions[index_best_score]
