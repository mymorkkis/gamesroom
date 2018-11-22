import pytest

from src.game import Coords
from src.game_enums import Color
from src.game_errors import IllegalMoveError
from src.othello_game import OthelloGame

def test_othello_board_setup():
    game = OthelloGame()
    expected_board_setup = set([(Color.WHITE, Coords(x=3, y=4)),
                                (Color.WHITE, Coords(x=4, y=3)),
                                (Color.BLACK, Coords(x=3, y=3)),
                                (Color.BLACK, Coords(x=4, y=4))])
    actual_board_setup = set(
        (disc.color, disc.coords)
        for row in game.board
        for disc in row if disc
    )
    assert actual_board_setup == expected_board_setup


def test_can_place_piece_and_trap_an_opponent_disc():
    game = OthelloGame()
    assert game.board[5][3] is None
    assert game.board[4][3].color == Color.WHITE

    game.move(Coords(x=5, y=3))
    assert game.board[5][3].color == Color.BLACK
    assert game.board[4][3].color == Color.BLACK


def test_player_color_swaps_for_each_turn():
    game = OthelloGame()
    assert game.playing_color == Color.BLACK

    game.move(Coords(x=5, y=3))
    assert game.playing_color == Color.WHITE

    game.move(Coords(x=5, y=4))
    assert game.playing_color == Color.BLACK


def test_illegal_disc_placement_raises_exception():
    game = OthelloGame()
    assert game.playing_color == Color.BLACK

    with pytest.raises(IllegalMoveError):
        game.move(Coords(x=5, y=4))

    with pytest.raises(IllegalMoveError):
        game.move(Coords(x=7, y=7))

    assert game.playing_color == Color.BLACK


def test_winner_declared():
    game = OthelloGame()
    game.discs_left = 1
    assert not game.winner

    game.move(Coords(x=5, y=3))
    assert game.winner == Color.BLACK


def test_drawer_declared():
    game = OthelloGame()
    game.discs_left = 2
    assert not game.winner

    game.move(Coords(x=5, y=3))
    game.move(Coords(x=5, y=2))
    assert game.winner == 'Draw'