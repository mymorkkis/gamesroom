"""Test module for game_errors."""
from collections import namedtuple

from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


Coords = namedtuple('Coords', 'x y')


def test_invalid_move_error():
    err_msg = 'Invalid move for this piece'
    try:
        raise InvalidMoveError(Coords(x=1, y=2), Coords(x=1, y=5), err_msg)
    except InvalidMoveError as err:
        assert err.from_coords == Coords(x=1, y=2)
        assert err.to_coords == Coords(x=1, y=5)
        assert err.message == err_msg
    

def test_not_on_board_error():
    err_msg = 'To_coordinates not valid board coordidnates'
    try:
        raise NotOnBoardError(Coords(x=1, y=5), err_msg)
    except NotOnBoardError as err:
        assert err.coords == Coords(x=1, y=5)
        assert err.message == err_msg


def test_piece_not_found_error():
    err_msg = 'No piece found at from_coordinates'
    try:
        raise PieceNotFoundError(Coords(x=1, y=2), err_msg)
    except PieceNotFoundError as err:
        assert err.coords == Coords(x=1, y=2)
        assert err.message == err_msg
