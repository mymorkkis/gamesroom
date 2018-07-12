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


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=4), True),   # Can move horizontally
    (Coords(x=7, y=6), True),   # Can move vertically
    (Coords(x=5, y=2), True),   # Can move diagonally
    (Coords(x=1, y=5), False),  # Can't move in non_linear direction
])
def test_queen_valid_move(queen, coords, rt_val):
    assert queen.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=4), True),   # Can capture horizontally
    (Coords(x=7, y=6), True),   # Can capture vertically
    (Coords(x=5, y=2), True),   # Can capture diagonally
    (Coords(x=1, y=5), False),  # Can't capture in non_linear direction
])
def test_queen_valid_capture(queen, coords, rt_val):
    assert queen.valid_capture(coords) == rt_val
