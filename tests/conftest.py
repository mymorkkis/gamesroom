"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import add, Coords
from src.game_pieces.king import King
from src.game_pieces.rook import Rook


@pytest.fixture(scope='function')
def new_game():
    """Return game with pieces set at new game starting postions."""
    new_chess_game = ChessGame()
    return new_chess_game


@pytest.fixture(scope='function')
def game():
    """Return game with empty board and Kings placed in corners.
       Kings are required so as not to throw errors.
       A game would always have Kings.
    """
    chess_game = ChessGame(restore_positions={})
    chess_game.add(King(Color.WHITE), Coords(x=0, y=0))
    chess_game.add(King(Color.BLACK), Coords(x=7, y=7))
    return chess_game


@pytest.fixture(scope='function')
def castle_game():
    """Return game with only King/Rook postions pre-set"""
    chess_game = ChessGame(restore_positions={})
    chess_game.add(King(Color.WHITE), Coords(x=4, y=0))
    chess_game.add(King(Color.BLACK), Coords(x=4, y=7))
    chess_game.add(Rook(Color.WHITE), Coords(x=0, y=0))
    chess_game.add(Rook(Color.WHITE), Coords(x=7, y=0))
    chess_game.add(Rook(Color.BLACK), Coords(x=0, y=7))
    chess_game.add(Rook(Color.BLACK), Coords(x=7, y=7))
    return chess_game
