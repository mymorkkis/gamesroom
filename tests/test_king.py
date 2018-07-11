"""Test module for King game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.king import King


@pytest.fixture(scope='module')
def king():
    """Setup King start coords. Return King"""
    chess_game = ChessGame()
    game_king = King(Color.BLACK)
    start_coords = Coords(x=1, y=1)
    chess_game.add(game_king, start_coords)
    return game_king


@pytest.mark.parametrize('coords, rt_val', [
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
])
def test_king_valid_move(king, coords, rt_val):
    assert king.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
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
])
def test_king_valid_capture(king, coords, rt_val):
    assert king.valid_capture(coords) == rt_val
