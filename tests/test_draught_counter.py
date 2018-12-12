import pytest

from src.games.game import Coords
from src.game_enums import Color
from src.game_pieces.draughts_counter import Counter


white_counter = Counter(Color.WHITE)
black_counter = Counter(Color.BLACK)


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=0, y=2), True),
    (Coords(x=2, y=2), True),
    (Coords(x=1, y=0), False),  # can't move horizontally
    (Coords(x=1, y=2), False),  # can't move vertically
    (Coords(x=0, y=0), False),  # can't move backwards
    (Coords(x=3, y=3), False)   # can't move more than one space
])
def test_white_counter_legal_move(coords, rt_val):
    white_counter.coords = Coords(x=1, y=1)
    assert white_counter.legal_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=7, y=5), True),
    (Coords(x=5, y=5), True),
    (Coords(x=7, y=6), False),  # can't move horizontally
    (Coords(x=6, y=5), False),  # can't move vertically
    (Coords(x=7, y=7), False),  # can't move backwards
    (Coords(x=4, y=4), False)   # can't move more than one space
])
def test_black_counter_legal_move(coords, rt_val):
    black_counter.coords = Coords(x=6, y=6)
    assert black_counter.legal_move(coords) == rt_val


@pytest.mark.parametrize('coords, rt_val', [
    (Coords(x=1, y=5), True),  # Any brown square potentially valid
    (Coords(x=6, y=5), False),  # Any white square is invalid capture
    (Coords(x=1, y=3), True),
    (Coords(x=4, y=5), False),
    (Coords(x=1, y=1), True),
    (Coords(x=4, y=3), False)
])
def test_counter_legal_capture(coords, rt_val):
    white_counter.coords = Coords(x=3, y=3)
    assert white_counter.legal_capture(coords) == rt_val
