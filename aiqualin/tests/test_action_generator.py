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

    new_piece_actions_left = ag.generate_actions_for_position_in_direction(
        col=2, row=2, d_col=-1, d_row=0, add_no_movement_action=False
    )
    assert len(new_piece_actions_left) == 2 * 35 * 6

    new_piece_actions_left_including_no_movement = (
        ag.generate_actions_for_position_in_direction(
            col=2, row=2, d_col=-1, d_row=0, add_no_movement_action=True
        )
    )

    assert len(new_piece_actions_left_including_no_movement) == 3 * 35 * 6

    new_piece_actions_right = ag.generate_actions_for_position_in_direction(
        col=2, row=2, d_col=1, d_row=0, add_no_movement_action=False
    )
    assert len(new_piece_actions_right) == 3 * 35 * 6

    new_piece_actions_right_including_no_movement = (
        ag.generate_actions_for_position_in_direction(
            col=2, row=2, d_col=1, d_row=0, add_no_movement_action=True
        )
    )
    assert len(new_piece_actions_right_including_no_movement) == 4 * 35 * 6

    actions = ag.generate_actions()

    assert (
        len(actions) == (10 + 1) * 35 * 6
    )  # can move current piece into 10 slots + 1 for leaving it where it is
    # then there are 35 empty spaces and 6 tiles to place


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

    new_piece_actions_left = ag.generate_actions_for_position_in_direction(
        col=0, row=0, d_col=-1, d_row=0, add_no_movement_action=False
    )
    assert len(new_piece_actions_left) == 0

    new_piece_actions_left_including_no_movement = (
        ag.generate_actions_for_position_in_direction(
            col=0, row=0, d_col=-1, d_row=0, add_no_movement_action=True
        )
    )
    assert len(new_piece_actions_left_including_no_movement) == 34 * 6

    new_piece_actions_right = ag.generate_actions_for_position_in_direction(
        col=0, row=0, d_col=1, d_row=0, add_no_movement_action=False
    )
    assert len(new_piece_actions_right) == 5 * 34 * 6

    new_piece_actions_right_including_no_movement = (
        ag.generate_actions_for_position_in_direction(
            col=0, row=0, d_col=1, d_row=0, add_no_movement_action=True
        )
    )
    assert len(new_piece_actions_right_including_no_movement) == 6 * 34 * 6

    actions = ag.generate_actions()
    # each existing piece can move to 10 positions, and there is the option
    # of not moving it at all, then there are 34 empty spaces for a new tile
    # to be placed and we can choose from 6 open tiles
    assert len(actions) == (10 + 10 + 1) * 34 * 6, len(actions)


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
    print()
    board.visualize()
    print()
    print()

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

    # the two tiles are next to each other, the old piece can only move to the right (horizontally) and the new piece can only move to the left (horizontally). The old piece has two empty tiles to its right and so does the new piece to its left. Vertically both pieces have 5 options
    ag = ActionGenerator(board=board, open_tiles=open_tiles, closed_tiles=closed_tiles)
    actions = ag.generate_actions()

    # plus 1 for not moving
    n_possible_moves = (2 + 5) + (2 + 5) + 1

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

    n_possible_moves = 10 + 10 + 1
    # one piece can move in all directions
    # other piece can move up, down, right, but not left because it was there the previous move

    assert len(actions) == n_possible_moves * 34 * 6


def test_endgame() -> None:
    board_str = """(1,3) (1,2) (5,2) (5,5) (5,3) (5,0)
(2,0) (2,2) (3,1) (3,0) (1,1) (5,1)
(0,2) (3,3) (1,5) (2,5) (4,2) (4,4)
(3,2) (2,3) (3,5) (4,1) (4,3) (5,4)
(0,1) (0,3) (0,5) (1,0) (4,0) (3,4)
(0,0) (0,4) (4,5) EMPTY (2,4) (1,4)"""

    board = Board.from_pretty_string(board_str)

    closed_tiles = []
    open_tiles = list(
        set(create_full_closed_tiles()) - set(chain.from_iterable(board.tiles))
    )

    print(closed_tiles, open_tiles)

    ag = ActionGenerator(
        board=board,
        open_tiles=open_tiles,
        closed_tiles=closed_tiles,
    )

    next_moves = ag.generate_actions()

    assert len(next_moves) == 4


# test_endgame()
