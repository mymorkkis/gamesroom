"""Test module for Bishop game piece."""
import pytest

from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.bishop import Bishop


@pytest.fixture(scope='module')
def bishop():
    """Setup Bishop start coords. Return Bishop"""
    game_bishop = Bishop(Color.BLACK)
    game_bishop.x_coord = 7
    game_bishop.y_coord = 4
    return game_bishop


test_data = [
    (Coords(x=5, y=2), True),   # Can move/capture diagonally
    (Coords(x=1, y=4), False),  # Can't move/capture horizontally
    (Coords(x=7, y=6), False),  # Can't move/capture vertically
    (Coords(x=1, y=5), False),  # Can't move/capture in non_linear direction
]

@pytest.mark.parametrize('coords, rt_val', test_data)
def test_bishop_valid_move(bishop, coords, rt_val):
    assert bishop.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_bishop_valid_capture(bishop, coords, rt_val):
    assert bishop.valid_capture(coords) == rt_val
