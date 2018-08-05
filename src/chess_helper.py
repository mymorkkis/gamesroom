"""Helper functions for ChessGame."""
from src.game_enums import Color
from src.game_enums import Direction
from src.game_helper import move_direction

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


def chess_piece_blocking(board, from_coords, to_coords):
    """Check if any piece blocking move from_coords to_coords. Return bool."""
    direction = move_direction(from_coords, to_coords)
    # Sort coords so logical direction of move not important
    # (x=5, y=6) -> (x=1, y=2) same as (x=1, y=2) -> (x=5, y=6)
    min_x_coord, max_x_coord = sorted([from_coords.x, to_coords.x])
    min_y_coord, max_y_coord = sorted([from_coords.y, to_coords.y])

    if direction == Direction.NON_LINEAR:
        # Only Knights move non_linear and they can jump over pieces
        return False
    elif direction == Direction.VERTICAL:
        for next_y_coord in range(min_y_coord + 1, max_y_coord):
            if board[from_coords.x][next_y_coord] is not None:
                return True
    elif direction == Direction.HORIZONTAL:
        for next_x_coord in range(min_x_coord + 1, max_x_coord):
            if board[next_x_coord][from_coords.y] is not None:
                return True
    elif direction == Direction.DIAGONAL:
        next_y_coord = min_y_coord + 1
        for next_x_coord in range(min_x_coord + 1, max_x_coord):
            if board[next_x_coord][next_y_coord] is not None:
                return True
            next_y_coord += 1 
        
    return False  # No piece blocking