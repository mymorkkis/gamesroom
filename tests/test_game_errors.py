"""Test module for game_errors."""
from src.game import Coords
from src.game_errors import IllegalMoveError, NotOnBoardError


def test_illegal_move_error():
    err_msg = 'Illegal move for this piece'
    try:
        raise IllegalMoveError(err_msg)
    except IllegalMoveError as err:
        assert err.message == err_msg


def test_not_on_board_error():
    err_msg = 'To_coordinates not legal board coordidnates'
    try:
        raise NotOnBoardError(Coords(x='z', y='10'), err_msg)
    except NotOnBoardError as err:
        assert err.coords == Coords(x='z', y='10')
        assert err.message == err_msg
