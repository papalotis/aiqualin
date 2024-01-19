from aiqualin.classes.action import Action
from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.game_scorer import GameScorer
from aiqualin.classes.tile import Tile


def test_empty_board():
    board = Board.empty_board()

    gs = GameScorer(board=board)

    assert gs.score == 0


def test_one_piece() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    gs = GameScorer(board=board)

    assert gs.score == 0


def test_two_pieces_same_animal() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.BLUE),
        )
    )

    board.visualize()

    gs = GameScorer(board=board)

    assert gs.score == 1


def test_two_pieces_same_color() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.JELLYFISH, color=Color.RED),
        )
    )

    board.visualize()

    gs = GameScorer(board=board)

    assert gs.score == -1


def test_three_pieces_same_color() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.JELLYFISH, color=Color.RED),
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=3,
            move_end_row=2,
            move_end_col=4,
            placement_row=2,
            placement_col=3,
            placement_tile=Tile(animal=Animal.STARFISH, color=Color.RED),
        )
    )

    board.visualize()

    gs = GameScorer(board=board)

    assert gs.score == -3


def test_four_pieces_where_we_have_a_sequence_of_two_broken_by_one() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.JELLYFISH, color=Color.RED),
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=3,
            move_end_row=2,
            move_end_col=4,
            placement_row=2,
            placement_col=3,
            placement_tile=Tile(animal=Animal.STARFISH, color=Color.RED),
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=4,
            move_end_row=2,
            move_end_col=5,
            placement_row=2,
            placement_col=4,
            placement_tile=Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        )
    )

    board.visualize()

    gs = GameScorer(board=board)

    assert gs.score == -1


def test_column_four_pieces_where_we_have_a_sequence_of_two_broken_by_one() -> None:
    board = Board.empty_board()

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.CRAB, color=Color.RED),
        )
    )

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=3,
            move_end_col=2,
            placement_row=2,
            placement_col=2,
            placement_tile=Tile(animal=Animal.JELLYFISH, color=Color.RED),
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=3,
            move_start_col=2,
            move_end_row=4,
            move_end_col=2,
            placement_row=3,
            placement_col=2,
            placement_tile=Tile(animal=Animal.STARFISH, color=Color.RED),
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=4,
            move_start_col=2,
            move_end_row=5,
            move_end_col=2,
            placement_row=4,
            placement_col=2,
            placement_tile=Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        )
    )

    board.visualize()

    gs = GameScorer(board=board)

    assert gs.score == -1


def test_board_from_manual() -> None:
    tiles = [
        [
            Tile(Animal.SEAHORSE, Color.RED),
            Tile(Animal.JELLYFISH, Color.GREEN),
            Tile(Animal.FISH, Color.GREEN),
            Tile(Animal.FISH, Color.BLUE),
            Tile(Animal.JELLYFISH, Color.BLUE),
            Tile(Animal.TURTLE, Color.PINK),
        ],
        [
            Tile(Animal.CRAB, Color.YELLOW),
            Tile(Animal.SEAHORSE, Color.YELLOW),
            Tile(Animal.FISH, Color.RED),
            Tile(Animal.SEAHORSE, Color.GREEN),
            Tile(Animal.TURTLE, Color.YELLOW),
            Tile(Animal.STARFISH, Color.BLUE),
        ],
        [
            Tile(Animal.STARFISH, Color.GREEN),
            Tile(Animal.SEAHORSE, Color.PURPLE),
            Tile(Animal.FISH, Color.YELLOW),
            Tile(Animal.SEAHORSE, Color.BLUE),
            Tile(Animal.CRAB, Color.BLUE),
            Tile(Animal.TURTLE, Color.BLUE),
        ],
        [
            Tile(Animal.STARFISH, Color.PURPLE),
            Tile(Animal.JELLYFISH, Color.YELLOW),
            Tile(Animal.SEAHORSE, Color.PINK),
            Tile(Animal.FISH, Color.PINK),
            Tile(Animal.JELLYFISH, Color.PINK),
            Tile(Animal.JELLYFISH, Color.RED),
        ],
        [
            Tile(Animal.STARFISH, Color.RED),
            Tile(Animal.STARFISH, Color.YELLOW),
            Tile(Animal.CRAB, Color.PURPLE),
            Tile(Animal.TURTLE, Color.GREEN),
            Tile(Animal.FISH, Color.PURPLE),
            Tile(Animal.TURTLE, Color.RED),
        ],
        [
            Tile(Animal.STARFISH, Color.PINK),
            Tile(Animal.CRAB, Color.GREEN),
            Tile(Animal.JELLYFISH, Color.PURPLE),
            Tile(Animal.TURTLE, Color.PURPLE),
            Tile(Animal.CRAB, Color.PINK),
            Tile(Animal.CRAB, Color.RED),
        ],
    ]

    board = Board(tiles=tiles)

    gs = GameScorer(board=board)

    assert gs.score_for_property(Animal) == 21
    assert gs.score_for_property(Color) == 19
    assert gs.score == 2

    # transpose the board
    # score should be the same
    tiles_transposed = list(zip(*tiles))
    board = Board(tiles=tiles_transposed)

    gs = GameScorer(board=board)

    assert gs.score_for_property(Animal) == 21
    assert gs.score_for_property(Color) == 19
    assert gs.score == 2


# test_board_from_manual()
