"""Test module for Pawn game piece."""
import pytest

from src.game_enums import Color
from src.game import Coords
from src.game_pieces.pawn import Pawn


@pytest.fixture(scope='module')
def black_pawn():
    """Setup Pawn start coords. Return Pawn"""
    pawn = Pawn(Color.BLACK)
    pawn.coords = Coords(x=1, y=6)
    return pawn


@pytest.fixture(scope='module')
def white_pawn():
    """Setup Pawn start coords. Return Pawn"""
    pawn = Pawn(Color.WHITE)
    pawn.coords = Coords(x=1, y=1)
    return pawn


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=5), True),   # Can move forward one space
    (Coords(x=1, y=4), True),   # 2 spaces forward allowed on first move
    (Coords(x=1, y=7), False),  # Can't move backwards
    (Coords(x=0, y=5), False),  # Can only move horizontally
    (Coords(x=2, y=5), False),
    (Coords(x=1, y=3), False)   # Can't move forward more than one (or two) spaces
])
def test_black_pawn_valid_move(black_pawn, coords, rt_val):
    assert black_pawn.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=2), True),   # Can move forward one space
    (Coords(x=1, y=3), True),   # 2 spaces forward allowed on first move
    (Coords(x=1, y=0), False),  # Can't move backwards
    (Coords(x=0, y=2), False),  # Can only move horizontally
    (Coords(x=2, y=2), False),
    (Coords(x=1, y=4), False)   # Can't move forward more than one (or two) spaces
])
def test_white_pawn_valid_move(white_pawn, coords, rt_val):
    assert white_pawn.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=2, y=5), True),   # Can capture one space diagonally
    (Coords(x=0, y=5), True),
    (Coords(x=0, y=4), False),  # Can't capture two spaces forward on first move
    (Coords(x=1, y=5), False),  # Can't capture forwards
    (Coords(x=1, y=7), False),  # Can't caputre backwards
    (Coords(x=3, y=4), False)   # Can't capture two spaces diagonally
])
def test_black_pawn_valid_capture(black_pawn, coords, rt_val):
    assert black_pawn.valid_capture(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=2, y=2), True),   # Can capture one space diagonally
    (Coords(x=0, y=2), True),
    (Coords(x=0, y=3), False),  # Can't capture two spaces forward on first move
    (Coords(x=1, y=2), False),  # Can't capture forwards
    (Coords(x=1, y=0), False),  # Can't caputre backwards
    (Coords(x=3, y=3), False)   # Can't capture two spaces diagonally
])
def test_white_pawn_valid_capture(white_pawn, coords, rt_val):
    assert white_pawn.valid_capture(coords) == rt_val
