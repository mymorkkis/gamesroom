"""Test module for Rook game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.rook import Rook


@pytest.fixture(scope='module')
def rook():
    """Setup Rook start coords. Return Rook"""
    chess_game = ChessGame()
    game_rook = Rook(Color.BLACK)
    start_coords = Coords(x=7, y=4)
    chess_game.add(game_rook, start_coords)
    return game_rook


def test_horizontal_move_valid(rook):
    valid = rook.valid_move(Coords(x=1, y=4))
    assert valid


def test_horizontal_capture_valid(rook):
    valid = rook.valid_capture(Coords(x=4, y=4))
    assert valid


def test_vertical_move_valid(rook):
    valid = rook.valid_move(Coords(x=7, y=6))
    assert valid


def test_vertical_capture_valid(rook):
    valid = rook.valid_capture(Coords(x=7, y=2))
    assert valid


def test_diagonal_move_not_valid(rook):
    valid = rook.valid_move(Coords(x=5, y=2))
    assert not valid


def test_nonlinear_capture_not_valid(rook):
    valid = rook.valid_capture(Coords(x=6, y=2))
    assert not valid
