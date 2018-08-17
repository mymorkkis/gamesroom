"""Shared pytest fixtures for test functions."""
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import add, Coords
from src.game_pieces.king import King
from src.game_pieces.pawn import Pawn


@pytest.fixture(scope='function')
def new_game():
    new_chess_game = ChessGame()
    return new_chess_game


@pytest.fixture(scope='function')
def game():
    chess_game = ChessGame(restore_positions={})
    return chess_game


@pytest.fixture(scope='function')
def piece(game):
    pawn = Pawn(Color.WHITE)
    start_coords = Coords(x=4, y=4)
    add(pawn, game.board, start_coords, game.pieces)
    return pawn


@pytest.fixture(scope='function')
def white_king(game):
    king = King(Color.WHITE)
    start_coords = Coords(x=2, y=2)
    add(king, game.board, start_coords, game.pieces)
    return king


# @pytest.fixture(scope='function')
# def black_king(game):
#     king = King(Color.WHITE)
#     start_coords = Coords(x=2, y=2)
#     add(king, game.board, start_coords, game.pieces)
