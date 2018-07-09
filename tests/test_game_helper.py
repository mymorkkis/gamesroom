"""Test module form game_helper module."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color, Direction
from src.game_helper import Coords, legal_start_position, move_direction, coord_errors
from src.game_pieces.pawn import Pawn
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


@pytest.fixture(scope='module')
def pawn():
    black_pawn = Pawn(Color.BLACK)
    chess_game = ChessGame()
    start_coords = Coords(x=4, y=4)
    chess_game.add(black_pawn, start_coords)
    return black_pawn


def test_move_direction_diagonal(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=6, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.DIAGONAL

    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=2, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.DIAGONAL


def test_move_direction_horizontal(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=2, y=4)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.HORIZONTAL

    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=6, y=4)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.HORIZONTAL


def test_move_direction_vertical(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=4, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.VERTICAL

    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=4, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.VERTICAL


def test_move_direction_non_linear(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=5, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.NON_LINEAR

    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=3, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.NON_LINEAR


def test_move_errors_return_false_if_no_errors(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=4, y=3)
    assert not coord_errors(pawn, from_coords, to_coords, 8, 8)


def test_invalid_from_coords_raises_exception(pawn):
    from_coords = Coords(x=1, y=50)  # From coordinates not on board
    to_coords = Coords(x=1, y=6)
    with pytest.raises(NotOnBoardError):
        coord_errors(pawn, from_coords, to_coords, 8, 8)


def test_invalid_to_coords_raises_exception(pawn):
    from_coords = Coords(x=pawn.x_coord, y=pawn.y_coord)
    to_coords = Coords(x=50, y=7)  # To coordinates not on board
    with pytest.raises(NotOnBoardError):
        coord_errors(pawn, from_coords, to_coords, 8, 8)


def test_same_from_and_to_coords_raise_exception(pawn):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=4)
    with pytest.raises(InvalidMoveError):
        coord_errors(pawn, from_coords, to_coords, 8, 8)


def test_no_piece_at_from_coords_raises_exception():
    from_coords = Coords(x=1, y=6)
    to_coords = Coords(x=1, y=5)
    with pytest.raises(PieceNotFoundError):
        # No piece passed to function
        coord_errors(None, from_coords, to_coords, 8, 8)


def test_legal_start_position():
    board = [[None] * 8 for _ in range(8)]
    pos = Coords(x=0, y=0)
    assert legal_start_position(board, pos)

    board[0][0] = 'Piece'
    assert not legal_start_position(board, pos)  # Place occupied

    with pytest.raises(NotOnBoardError):
        pos = Coords(x=9, y=9)
        legal_start_position(board, pos)
