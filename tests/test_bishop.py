"""Test module for Bishop game piece."""
import pytest

from src.game_enums import Color
from src.games.game import Coords
from src.game_pieces.bishop import Bishop


@pytest.fixture(scope='module')
def bishop():
    """Setup Bishop start coords. Return Bishop"""
    game_bishop = Bishop(Color.BLACK)
    game_bishop.coords = Coords(x=7, y=4)
    return game_bishop


test_data = [
    (Coords(x=5, y=2), True),   # Can move/capture diagonally
    (Coords(x=1, y=4), False),  # Can't move/capture horizontally
    (Coords(x=7, y=6), False),  # Can't move/capture vertically
    (Coords(x=1, y=5), False),  # Can't move/capture in non_linear direction
]

@pytest.mark.parametrize('coords, rt_val', test_data)
def test_bishop_legal_move(bishop, coords, rt_val):
    assert bishop.legal_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_bishop_legal_capture(bishop, coords, rt_val):
    assert bishop.legal_capture(coords) == rt_val
