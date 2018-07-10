"""Test module form game_helper module."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color, Direction
from src.game_helper import (chess_piece_blocking, coord_errors, Coords, 
                             legal_start_position, move_direction)
from src.game_pieces.pawn import Pawn
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


@pytest.fixture(scope='module')
def game():
    chess_game = ChessGame()
    return chess_game


@pytest.fixture(scope='module')
def piece(game):
    pawn = Pawn(Color.BLACK)
    start_coords = Coords(x=4, y=4)
    game.add(pawn, start_coords)
    return pawn


def test_move_direction_diagonal(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=6, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.DIAGONAL

    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=2, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.DIAGONAL


def test_move_direction_horizontal(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=2, y=4)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.HORIZONTAL

    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=6, y=4)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.HORIZONTAL


def test_move_direction_vertical(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=4, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.VERTICAL

    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=4, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.VERTICAL


def test_move_direction_non_linear(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=5, y=6)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.NON_LINEAR

    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=3, y=2)
    direction = move_direction(from_coords, to_coords)
    assert direction == Direction.NON_LINEAR


def test_legal_start_position():
    board = [[None] * 8 for _ in range(8)]
    pos = Coords(x=0, y=0)
    assert legal_start_position(board, pos)

    board[0][0] = 'Piece'
    assert not legal_start_position(board, pos)  # Place occupied

    with pytest.raises(NotOnBoardError):
        pos = Coords(x=9, y=9)
        legal_start_position(board, pos)


def test_coord_errors_returns_false_if_no_errors(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=4, y=3)
    assert not coord_errors(piece, from_coords, to_coords, 8, 8)


def test_invalid_from_coords_raises_exception(piece):
    from_coords = Coords(x=1, y=50)  # From coordinates not on board
    to_coords = Coords(x=1, y=6)
    with pytest.raises(NotOnBoardError):
        coord_errors(piece, from_coords, to_coords, 8, 8)


def test_invalid_to_coords_raises_exception(piece):
    from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
    to_coords = Coords(x=50, y=7)  # To coordinates not on board
    with pytest.raises(NotOnBoardError):
        coord_errors(piece, from_coords, to_coords, 8, 8)


def test_same_from_and_to_coords_raise_exception(piece):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=4)
    with pytest.raises(InvalidMoveError):
        coord_errors(piece, from_coords, to_coords, 8, 8)


def test_no_piece_at_from_coords_raises_exception():
    from_coords = Coords(x=1, y=6)
    to_coords = Coords(x=1, y=5)
    with pytest.raises(PieceNotFoundError):
        # No piece passed to function
        coord_errors(None, from_coords, to_coords, 8, 8)


def test_piece_blocking_diagonal_move_returns_true(game):
    # Pawn at Coords(4, 4)
    from_coords = Coords(x=3, y=3)
    to_coords = Coords(x=6, y=6)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=6)
    to_coords = Coords(x=3, y=3)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_horizontal_move_returns_true(game):
    # Pawn at Coords(4, 4)
    from_coords = Coords(x=2, y=4)
    to_coords = Coords(x=6, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=4)
    to_coords = Coords(x=2, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_vertical_move_returns_true(game):
    # Pawn at Coords(4, 4)
    from_coords = Coords(x=4, y=2)
    to_coords = Coords(x=4, y=6)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=6)
    to_coords = Coords(x=4, y=2)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_non_linear_move_returns_false(game):
    # Pawn at Coords(4, 4)
    from_coords = Coords(x=3, y=3)
    to_coords = Coords(x=4, y=5)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=5)
    to_coords = Coords(x=3, y=3)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)


def test_no_piece_blocking_returns_false(game):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=6)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)
