"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import add, Coords
from src.game_pieces.king import King


@pytest.fixture(scope='function')
def new_game():
    new_chess_game = ChessGame()
    return new_chess_game


@pytest.fixture(scope='function')
def game():
    chess_game = ChessGame(restore_positions={})
    # Start game with Kings for testing. Game with no Kings causes errors.
    add(King(Color.WHITE), chess_game, Coords(x=4, y=0))
    add(King(Color.BLACK), chess_game, Coords(x=4, y=7))
    return chess_game
