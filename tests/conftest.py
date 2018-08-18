"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame


@pytest.fixture(scope='function')
def new_game():
    new_chess_game = ChessGame()
    return new_chess_game


@pytest.fixture(scope='function')
def game():
    chess_game = ChessGame(restore_positions={})
    return chess_game
