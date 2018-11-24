import pytest

from src.game_enums import Color
from src.game import Coords
from src.draughts_game import DraughtsGame
from src.game_pieces.draughts_counter import Counter
from src.game_errors import IllegalMoveError


def test_draughts_setup_correctly():
    game = DraughtsGame()
    expected_board_setup = set([
        (Color.WHITE, Coords(x=0, y=0)),
        (Color.WHITE, Coords(x=2, y=0)),
        (Color.WHITE, Coords(x=4, y=0)),
        (Color.WHITE, Coords(x=6, y=0)),
        (Color.WHITE, Coords(x=1, y=1)),
        (Color.WHITE, Coords(x=3, y=1)),
        (Color.WHITE, Coords(x=5, y=1)),
        (Color.WHITE, Coords(x=7, y=1)),
        (Color.WHITE, Coords(x=0, y=2)),
        (Color.WHITE, Coords(x=2, y=2)),
        (Color.WHITE, Coords(x=4, y=2)),
        (Color.WHITE, Coords(x=6, y=2)),
        (Color.BLACK, Coords(x=1, y=5)),
        (Color.BLACK, Coords(x=3, y=5)),
        (Color.BLACK, Coords(x=5, y=5)),
        (Color.BLACK, Coords(x=7, y=5)),
        (Color.BLACK, Coords(x=0, y=6)),
        (Color.BLACK, Coords(x=2, y=6)),
        (Color.BLACK, Coords(x=4, y=6)),
        (Color.BLACK, Coords(x=6, y=6)),
        (Color.BLACK, Coords(x=1, y=7)),
        (Color.BLACK, Coords(x=3, y=7)),
        (Color.BLACK, Coords(x=5, y=7)),
        (Color.BLACK, Coords(x=7, y=7))
    ])
    actual_board_setup = set(
        (counter.color, counter.coords)
        for row in game.board
        for counter in row if counter
    )
    assert actual_board_setup == expected_board_setup


def test_draughts_piece_can_move():
    game = DraughtsGame()
    assert game.board[5][3] is None

    game.move(Coords(x=4, y=2), Coords(x=5, y=3))
    assert game.board[4][2] is None
    assert game.board[5][3] == Counter(Color.WHITE)


def test_illegal_move_raises_exception():
    game = DraughtsGame()

    with pytest.raises(IllegalMoveError):
        game.move(Coords(x=4, y=2), Coords(x=4, y=3))


def test_draughts_piece_can_capture():
    game = DraughtsGame({})  # empty board
    game.add(Counter(Color.WHITE), Coords(x=0, y=0))
    game.add(Counter(Color.BLACK), Coords(x=1, y=1))
    game.move(Coords(x=0, y=0), Coords(x=2, y=2))

    assert game.board[1][1] is None
    assert game.board[2][2] == Counter(Color.WHITE)