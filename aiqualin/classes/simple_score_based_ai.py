from aiqualin.classes.action import Action
from aiqualin.classes.action_generator import ActionGenerator
from aiqualin.classes.board import Board
from aiqualin.classes.player import AbstractPlayer
from aiqualin.classes.tile import Tile
from aiqualin.classes.timer import Timer


class SimpleScoreBasedAI(AbstractPlayer):
    def score_board(self, board: Board) -> int:
        our_score = self.our_score(board)
        their_score = self.their_score(board)

        return our_score - their_score

    def next_action(
        self, board: Board, open_tiles: list[Tile], closed_tiles: list[Tile]
    ) -> Action:
        no_print = True

        with Timer("generator", no_print=no_print):
            next_actions = list(
                ActionGenerator(board, open_tiles, closed_tiles).generate_actions()
            )

        print(f"There are {len(next_actions)} possible actions")

        with Timer("move_application", no_print=no_print):
            next_boards = [board.apply_action(action) for action in next_actions]

        with Timer("scoring", no_print=no_print):
            next_scores = [self.score_board(next_board) for next_board in next_boards]

        index_best_score = next_scores.index(max(next_scores))

        return next_actions[index_best_score]
