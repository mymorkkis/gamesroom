"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import add, Coords
from src.game_pieces.king import King
from src.game_pieces.rook import Rook


@pytest.fixture(scope='function')
def new_game():
    # Start with full chess starting postions
    new_chess_game = ChessGame()
    return new_chess_game


@pytest.fixture(scope='function')
def game():
    # Start with new board and pre set postions to test castling
    chess_game = ChessGame(restore_positions={})
    add(King(Color.WHITE), chess_game, Coords(x=4, y=0))
    add(King(Color.BLACK), chess_game, Coords(x=4, y=7))
    add(Rook(Color.WHITE), chess_game, Coords(x=0, y=0))
    add(Rook(Color.WHITE), chess_game, Coords(x=7, y=0))
    add(Rook(Color.BLACK), chess_game, Coords(x=7, y=7))
    add(Rook(Color.BLACK), chess_game, Coords(x=7, y=7))
    return chess_game
