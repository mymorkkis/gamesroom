"""Test module."""
# from itertools import product

from src.game_enums import Color
from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King 
from src.game_pieces.knight import Knight 
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


def new_chess_setup():
    """Return dictionary of new chess game default piece postitions. 
       
       Dictionary is in following format:
       key = str representation of game coordinates xy
       value = chess GamePiece
       e.g '00': Rook(Color.WHITE)
    """
    white_pieces = _new_chess_pieces(Color.WHITE, y_idxs=[0, 1])
    black_pieces = _new_chess_pieces(Color.BLACK, y_idxs=[7, 6])
    return dict(white_pieces + black_pieces)


def _new_chess_pieces(color, *, y_idxs=None):
    """Helper method for new_chess_setup."""
    coords = [f'{x_idx}{y_idx}' for y_idx in y_idxs for x_idx in range(8)]
    pieces = [
        Rook(color),
        Knight(color),
        Bishop(color),
        Queen(color),
        King(color),
        Bishop(color),
        Knight(color),
        Rook(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color)
    ]
    return list(zip(coords, pieces))
