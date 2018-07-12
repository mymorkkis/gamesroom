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


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=4), True),   # Can move horizontally
    (Coords(x=7, y=6), True),   # Can move vertically
    (Coords(x=5, y=2), False),  # Can't move diagonally
    (Coords(x=1, y=5), False),  # Can't move in non_linear direction
])
def test_rook_valid_move(rook, coords, rt_val):
    assert rook.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=4), True),   # Can capture horizontally
    (Coords(x=7, y=6), True),   # Can capture vertically
    (Coords(x=5, y=2), False),  # Can't capture diagonally
    (Coords(x=1, y=5), False),  # Can't capture in non_linear direction
])
def test_rook_valid_capture(rook, coords, rt_val):
    assert rook.valid_capture(coords) == rt_val
