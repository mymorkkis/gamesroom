"""Test module for Queen game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.queen import Queen


@pytest.fixture(scope='module')
def queen():
    """Setup Queen start coords. Return Queen"""
    chess_game = ChessGame()
    game_queen = Queen(Color.BLACK)
    start_coords = Coords(x=7, y=4)
    chess_game.add(game_queen, start_coords)
    return game_queen


def test_horizontal_move_valid(queen):
    valid = queen.valid_move(Coords(x=1, y=4))
    assert valid


def test_vertical_capture_valid(queen):
    valid = queen.valid_capture(Coords(x=7, y=6))
    assert valid


def test_diagonal_move_valid(queen):
    valid = queen.valid_move(Coords(x=5, y=2))
    assert valid


def test_nonlinear_move_not_valid(queen):
    valid = queen.valid_move(Coords(x=1, y=5))
    assert not valid


def test_nonlinear_capture_not_valid(queen):
    valid = queen.valid_move(Coords(x=6, y=2))
    assert not valid
