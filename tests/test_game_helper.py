"""Test module form game_helper module."""
from collections import namedtuple
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color, Direction
from src.game_helper import move_direction
from src.game_pieces.pawn import Pawn


Coords = namedtuple('Coords', 'x y')

@pytest.fixture(scope='module')
def pawn():
    black_pawn = Pawn(Color.BLACK)
    chess_game = ChessGame()
    start_coords = Coords(x=4, y=4)
    chess_game.add(black_pawn, start_coords)
    return black_pawn

def test_move_direction_diagonal_down(pawn):
    to_coords = Coords(x=6, y=6)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.DIAGONAL

def test_move_direction_diagonal_up(pawn):
    to_coords = Coords(x=2, y=2)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.DIAGONAL

def test_move_direction_horizontal_down(pawn):
    to_coords = Coords(x=2, y=4)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.HORIZONTAL

def test_move_direction_horizontal_up(pawn):
    to_coords = Coords(x=6, y=4)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.HORIZONTAL

def test_move_direction_vertical_down(pawn):
    to_coords = Coords(x=4, y=2)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.VERTICAL

def test_move_direction_vertical_up(pawn):
    to_coords = Coords(x=4, y=6)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.VERTICAL

def test_move_direction_non_linear(pawn):
    to_coords = Coords(x=5, y=6)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.NON_LINEAR

    to_coords = Coords(x=3, y=2)
    direction = move_direction(pawn, to_coords)
    assert direction == Direction.NON_LINEAR
