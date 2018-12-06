"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
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
    chess_game = ChessGame(restore_positions={
        '00': King(Color.WHITE),
        '77': King(Color.BLACK)
    })
    return chess_game


@pytest.fixture(scope='function')
def castle_game():
    """Return game with only King/Rook postions pre-set"""
    chess_game = ChessGame(restore_positions={
        '40': King(Color.WHITE),
        '47': King(Color.BLACK),
        '00': Rook(Color.WHITE),
        '70': Rook(Color.WHITE),
        '07': Rook(Color.BLACK),
        '77': Rook(Color.BLACK)
    })
    return chess_game
