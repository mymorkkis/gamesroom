"""Test module for Knight game piece."""
import pytest

from src.game_enums import Color
from src.games.game import Coords
from src.game_pieces.knight import Knight


@pytest.fixture(scope='module')
def knight():
    """Setup Knight start coords. Return Knight"""
    game_knight = Knight(Color.BLACK)
    game_knight.coords = Coords(x=4, y=4)
    return game_knight


test_data = [
    (Coords(x=5, y=6), True),
    (Coords(x=5, y=2), True),
    (Coords(x=6, y=5), True),
    (Coords(x=6, y=3), True),
    (Coords(x=3, y=6), True),
    (Coords(x=3, y=2), True),
    (Coords(x=2, y=5), True),
    (Coords(x=2, y=3), True),
    (Coords(x=4, y=6), False),  # Can't move/capture vertically
    (Coords(x=2, y=4), False),  # Can't move/capture horizontally
    (Coords(x=5, y=5), False),  # Can't move/capture diagonally
    (Coords(x=2, y=8), False),  # Can't move/capture non_linear movement more than 3 spaces
]


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_knight_legal_move(knight, coords, rt_val):
    assert knight.legal_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_knight_legal_capture(knight, coords, rt_val):
    assert knight.legal_capture(coords) == rt_val
