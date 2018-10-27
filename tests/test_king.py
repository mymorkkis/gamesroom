"""Test module for King game piece."""
import pytest

from src.game_enums import Color
from src.game import Coords
from src.game_pieces.king import King


@pytest.fixture(scope='module')
def king():
    """Setup King start coords. Return King"""
    game_king = King(Color.BLACK)
    game_king.coords = Coords(x=1, y=1)
    return game_king


test_data = [
    (Coords(x=0, y=0), True),
    (Coords(x=1, y=0), True),
    (Coords(x=2, y=0), True),
    (Coords(x=0, y=1), True),
    (Coords(x=1, y=1), False),  # Same position
    (Coords(x=2, y=1), True),
    (Coords(x=0, y=2), True),
    (Coords(x=1, y=2), True),
    (Coords(x=2, y=2), True),
    (Coords(x=0, y=3), False),  # All more than one space
    (Coords(x=3, y=3), False),
    (Coords(x=3, y=0), False),
]


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_king_valid_move(king, coords, rt_val):
    assert king.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_king_valid_capture(king, coords, rt_val):
    assert king.valid_capture(coords) == rt_val
