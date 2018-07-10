"""Test module for Bishop game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.bishop import Bishop


@pytest.fixture(scope='module')
def bishop():
    """Setup Bishop start coords. Return Bishop"""
    chess_game = ChessGame()
    game_bishop = Bishop(Color.BLACK)
    start_coords = Coords(x=7, y=4)
    chess_game.add(game_bishop, start_coords)
    return game_bishop


def test_diagonal_move_valid(bishop):
    valid = bishop.valid_move(Coords(x=5, y=2))
    assert valid


def test_diagonal_capture_valid(bishop):
    valid = bishop.valid_capture(Coords(x=4, y=1))
    assert valid


def test_horizontal_move_not_valid(bishop):
    valid = bishop.valid_move(Coords(x=1, y=4))
    assert not valid


def test_vertical_capture_not_valid(bishop):
    valid = bishop.valid_capture(Coords(x=7, y=2))
    assert not valid


def test_nonlinear_move_not_valid(bishop):
    valid = bishop.valid_move(Coords(x=6, y=2))
    assert not valid
