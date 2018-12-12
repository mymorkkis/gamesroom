"""Test module for Queen game piece."""
import pytest

from src.game_enums import Color
from src.games.game import Coords
from src.game_pieces.queen import Queen


@pytest.fixture(scope='module')
def queen():
    """Setup Queen start coords. Return Queen"""
    game_queen = Queen(Color.BLACK)
    game_queen.coords = Coords(x=7, y=4)
    return game_queen


test_data = [
    (Coords(x=1, y=4), True),   # Can move/capture horizontally
    (Coords(x=7, y=6), True),   # Can move/capture vertically
    (Coords(x=5, y=2), True),   # Can move/capture diagonally
    (Coords(x=1, y=5), False),  # Can't move/capture in non_linear direction
]


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_queen_legal_move(queen, coords, rt_val):
    assert queen.legal_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', test_data)
def test_queen_legal_capture(queen, coords, rt_val):
    assert queen.legal_capture(coords) == rt_val
