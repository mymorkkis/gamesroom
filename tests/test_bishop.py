"""Test module for Bishop game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.bishop import Bishop


@pytest.fixture(scope='module')
def bishop():
    """Setup Bishop start coords. Return Bishop"""
    chess_game = ChessGame()
    game_bishop = Bishop(Color.BLACK)
    start_coords = Coords(x=7, y=4)
    chess_game.add(game_bishop, start_coords)
    return game_bishop


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=5, y=2), True),   # Can move diagonally
    (Coords(x=1, y=4), False),  # Can't move horizontally
    (Coords(x=7, y=6), False),  # Can't move vertically
    (Coords(x=1, y=5), False),  # Can't move in non_linear direction
])
def test_bishop_valid_move(bishop, coords, rt_val):
    assert bishop.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=5, y=2), True),   # Can capture diagonally
    (Coords(x=1, y=4), False),  # Can't capture horizontally
    (Coords(x=7, y=6), False),  # Can't capture vertically
    (Coords(x=1, y=5), False),  # Can't capture in non_linear direction
])
def test_bishop_valid_capture(bishop, coords, rt_val):
    assert bishop.valid_capture(coords) == rt_val
