"""Test module for Pawn game piece."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.pawn import Pawn


@pytest.fixture(scope='module')
def black_pawn():
    game = ChessGame()
    start_coords = Coords(x=1, y=6)
    pawn = Pawn(Color.BLACK)
    game.add(pawn, start_coords)
    return pawn


@pytest.fixture(scope='module')
def white_pawn():
    game = ChessGame()
    start_coords = Coords(x=1, y=1)
    pawn = Pawn(Color.WHITE)
    game.add(pawn, start_coords)
    return pawn


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=5), True),
    # TODO Add test to confirm 2 spaces on first move
    (Coords(x=1, y=7), False),
    (Coords(x=0, y=5), False),
    (Coords(x=2, y=5), False),
    (Coords(x=1, y=3), False)
])
def test_black_pawn_valid_move(black_pawn, coords, rt_val):
    assert black_pawn.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=2), True),
    # TODO Add test to confirm 2 spaces on first move
    (Coords(x=1, y=0), False),
    (Coords(x=0, y=2), False),
    (Coords(x=2, y=2), False),
    (Coords(x=1, y=4), False)
])
def test_white_pawn_valid_move(white_pawn, coords, rt_val):
    assert white_pawn.valid_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=2, y=5), True),
    (Coords(x=0, y=5), True),
    (Coords(x=1, y=5), False),
    (Coords(x=1, y=7), False),
    (Coords(x=1, y=6), False)
])
def test_black_pawn_valid_capture(black_pawn, coords, rt_val):
    assert black_pawn.valid_capture(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=2, y=2), True),
    (Coords(x=0, y=2), True),
    (Coords(x=1, y=2), False),
    (Coords(x=1, y=0), False),
    (Coords(x=1, y=1), False)
])
def test_white_pawn_valid_capture(white_pawn, coords, rt_val):
    assert white_pawn.valid_capture(coords) == rt_val
