"""Test module for Rook game piece."""
import pytest

from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.rook import Rook


@pytest.fixture(scope='module')
def rook():
    """Setup Rook start coords. Return Rook"""
    game_rook = Rook(Color.BLACK)
    game_rook.x_coord = 7
    game_rook.y_coord = 4
    return game_rook


test_data = [
    (Coords(x=1, y=4), True),   # Can move/capture horizontally
    (Coords(x=7, y=6), True),   # Can move/capture vertically
    (Coords(x=5, y=2), False),  # Can't move/capture diagonally
    (Coords(x=1, y=5), False),  # Can't move/capture in non_linear direction
]


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_rook_valid_move(rook, coords, rt_val):
    assert rook.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_rook_valid_capture(rook, coords, rt_val):
    assert rook.valid_capture(coords) == rt_val
