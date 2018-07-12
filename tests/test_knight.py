"""Test module for Knight game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.knight import Knight


@pytest.fixture(scope='module')
def knight():
    """Setup Knight start coords. Return Knight"""
    chess_game = ChessGame()
    game_knight = Knight(Color.BLACK)
    start_coords = Coords(x=4, y=4)
    chess_game.add(game_knight, start_coords)
    return game_knight


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=5, y=6), True),
    (Coords(x=5, y=2), True),
    (Coords(x=6, y=5), True),
    (Coords(x=6, y=3), True),
    (Coords(x=3, y=6), True),
    (Coords(x=3, y=2), True),  
    (Coords(x=2, y=5), True),
    (Coords(x=2, y=3), True),
    (Coords(x=4, y=6), False),  # Can't move vertically
    (Coords(x=2, y=4), False),  # Can't move horizontally
    (Coords(x=5, y=5), False),  # Can't move diagonally
    (Coords(x=2, y=8), False),  # Can't move non_linear movement more than 3 spaces
])
def test_knight_valid_move(knight, coords, rt_val):
    assert knight.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=5, y=6), True),
    (Coords(x=5, y=2), True),
    (Coords(x=6, y=5), True),
    (Coords(x=6, y=3), True),
    (Coords(x=3, y=6), True),
    (Coords(x=3, y=2), True),  
    (Coords(x=2, y=5), True),
    (Coords(x=2, y=3), True),
    (Coords(x=4, y=6), False),  # Can't capture vertically
    (Coords(x=2, y=4), False),  # Can't capture horizontally
    (Coords(x=5, y=5), False),  # Can't capture diagonally
    (Coords(x=2, y=8), False),  # Can't capture non_linear movement more than 3 spaces
])
def test_knight_valid_capture(knight, coords, rt_val):
    assert knight.valid_capture(coords) == rt_val
