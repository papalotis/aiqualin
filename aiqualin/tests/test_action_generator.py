from itertools import chain

from aiqualin.classes.action import Action
from aiqualin.classes.action_generator import ActionGenerator
from aiqualin.classes.animal import Animal
from aiqualin.classes.board import Board
from aiqualin.classes.color import Color
from aiqualin.classes.game import create_full_closed_tiles
from aiqualin.classes.tile import Tile


def test_start_moves():
    board = Board.empty_board()

    tiles_to_place = [
        Tile(animal=Animal.CRAB, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.BLUE),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.STARFISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    open_tiles = tiles_to_place.copy()
    closed_tiles = list(set(create_full_closed_tiles()) - set(tiles_to_place))
    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)

    actions = ag.generate_actions()

    assert len(actions) == 6 * 6 * 6  # six tiles, six rows and six columns

    expected_actions = {
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=i,
            placement_col=j,
            placement_tile=tile,
        )
        for i in range(6)
        for j in range(6)
        for tile in tiles_to_place
    }

    assert actions == expected_actions


def test_move_with_one_tile_placed():
    board = Board.empty_board()

    tile_already_placed = Tile(animal=Animal.CRAB, color=Color.RED)

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=tile_already_placed,
        )
    )

    open_tiles = [
        Tile(animal=Animal.JELLYFISH, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.BLUE),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.STARFISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    closed_tiles = list(
        set(create_full_closed_tiles()) - set(open_tiles) - {tile_already_placed}
    )

    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)

    actions = ag.generate_actions()

    assert (
        len(actions) == (2 + 2) * 35 * 6
    )  # can move one piece in all 4 directions and can place one of 6 tiles in the 35 empty positions


def test_move_with_two_tiles_placed_1():
    board = Board.empty_board()

    tile_already_placed = [
        Tile(animal=Animal.CRAB, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.BLUE),
    ]

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=tile_already_placed[0],
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=0,
            placement_col=0,
            placement_tile=tile_already_placed[1],
        )
    )

    board.visualize()

    open_tiles = [
        Tile(animal=Animal.JELLYFISH, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.PINK),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.STARFISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    closed_tiles = list(
        set(create_full_closed_tiles()) - set(open_tiles) - set(tile_already_placed)
    )

    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)

    actions = ag.generate_actions()

    n_possible_moves = 1 + 1 + 2 + 1
    # one piece is top left so it can only move down and right
    # other piece can move up, down, right, but not left because it was there the previous move

    assert len(actions) == n_possible_moves * 34 * 6


def test_move_with_two_tiles_placed_2():
    board = Board.empty_board()

    tile_already_placed = [
        Tile(animal=Animal.CRAB, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.BLUE),
    ]

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=tile_already_placed[0],
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=2,
            placement_col=2,
            placement_tile=tile_already_placed[1],
        )
    )

    board.visualize()

    open_tiles = [
        Tile(animal=Animal.JELLYFISH, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.PINK),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.STARFISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    closed_tiles = list(
        set(create_full_closed_tiles()) - set(open_tiles) - set(tile_already_placed)
    )

    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)

    actions = ag.generate_actions()

    n_possible_moves = 1 + 2 + 2 + 1
    # one piece is all but right, because the other piece is there
    # other piece can move up, down, right, but not left because it was there the previous move and because the other piece is there

    assert len(actions) == n_possible_moves * 34 * 6


def test_move_with_two_tiles_placed_3():
    board = Board.empty_board()

    tile_already_placed = [
        Tile(animal=Animal.CRAB, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.BLUE),
    ]

    board = board.apply_action(
        Action(
            move_start_row=-1,
            move_start_col=-1,
            move_end_row=-1,
            move_end_col=-1,
            placement_row=2,
            placement_col=2,
            placement_tile=tile_already_placed[0],
        )
    )

    board.visualize()

    board = board.apply_action(
        Action(
            move_start_row=2,
            move_start_col=2,
            move_end_row=2,
            move_end_col=3,
            placement_row=1,
            placement_col=1,
            placement_tile=tile_already_placed[1],
        )
    )

    board.visualize()

    open_tiles = [
        Tile(animal=Animal.JELLYFISH, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.PINK),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.STARFISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    closed_tiles = list(
        set(create_full_closed_tiles()) - set(open_tiles) - set(tile_already_placed)
    )

    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)

    actions = ag.generate_actions()

    n_possible_moves = 2 + 2 + 2 + 1
    # one piece can move in all directions
    # other piece can move up, down, right, but not left because it was there the previous move

    assert len(actions) == n_possible_moves * 34 * 6


def test_specific_board() -> None:
    board_str = """EMPTY EMPTY EMPTY EMPTY EMPTY EMPTY
EMPTY EMPTY EMPTY EMPTY EMPTY EMPTY
EMPTY EMPTY EMPTY EMPTY (4,5) EMPTY
EMPTY EMPTY EMPTY EMPTY EMPTY EMPTY
EMPTY EMPTY EMPTY EMPTY EMPTY EMPTY
EMPTY EMPTY EMPTY (5,5) EMPTY EMPTY"""

    last_action = Action(
        move_start_row=1,
        move_start_col=4,
        move_end_row=2,
        move_end_col=4,
        placement_row=5,
        placement_col=3,
        placement_tile=Tile(animal=Animal.TURTLE, color=Color.YELLOW),
    )

    board = Board.from_pretty_string(board_str, last_action)
    board.visualize()

    open_tiles = [
        Tile(animal=Animal.JELLYFISH, color=Color.RED),
        Tile(animal=Animal.JELLYFISH, color=Color.PINK),
        Tile(animal=Animal.FISH, color=Color.GREEN),
        Tile(animal=Animal.FISH, color=Color.YELLOW),
        Tile(animal=Animal.SEAHORSE, color=Color.PINK),
        Tile(animal=Animal.TURTLE, color=Color.PURPLE),
    ]

    closed_tiles = list(
        set(create_full_closed_tiles())
        - set(open_tiles)
        - set(chain.from_iterable(board.tiles))
    )

    actions = ActionGenerator(
        board=board, open_tiles=open_tiles, closed_tiles=closed_tiles
    ).generate_actions()

    assert (
        sum(
            action.move_end_col != last_action.move_start_col
            or action.move_end_row != last_action.move_start_row
            for action in actions
            if action.placement_tile == open_tiles[0]
        )
        == 0
    )


# test_specific_board()
