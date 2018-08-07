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


def king_in_check(king_coords, board, *, opponent_color=None):
    if opponent_color == Color.WHITE and _white_pawn_check(king_coords, board):
        return True
    if opponent_color == Color.BLACK and _black_pawn_check(king_coords, board):
        return True
    if _knight_check(king_coords, board, opponent_color):
        return True
    if _check_by_other_piece(king_coords, board, opponent_color):
        return True
    return False  # King not in check


def _white_pawn_check(king_coords, board):
    x, y = king_coords
    pawn = Pawn(Color.WHITE)
    return board[y + 1][x + 1] == pawn or board[y + 1][x - 1] == pawn


def _black_pawn_check(king_coords, board):
    x, y = king_coords
    pawn = Pawn(Color.BLACK)
    return board[y - 1][x + 1] == pawn or board[y - 1][x - 1] == pawn


def _knight_check(king_coords, board, opponent_color):
    x, y = king_coords
    knight = Knight(opponent_color)
    return (board[x + 1][y + 2] == knight
            or board[x + 1][y - 2] == knight
            or board[x + 2][y + 1] == knight
            or board[x + 2][y - 1] == knight
            or board[x - 1][y + 2] == knight
            or board[x - 1][y - 2] == knight
            or board[x - 2][y + 1] == knight
            or board[x - 2][y - 1] == knight)


def _check_by_other_piece(king_coords, board, opponent_color):
    for direction in DIRECTIONS:
        next_x, next_y = king_coords
        king_is_threat = True
        try:
            while True:
                next_x, next_y = NEXT_MOVE_COORD[direction](next_x, next_y)
                piece = board[next_x][next_y]
                if piece and piece.color != opponent_color:
                    continue  # Own piece blocking possible check from this direction
                if piece and piece.color == opponent_color:
                    if piece.type == 'King' and king_is_threat:
                        return True
                    elif direction in {'N', 'E', 'S', 'W'} and piece.type in {'Rook', 'Queen'}:
                        return True
                    elif direction in {'NE', 'SE', 'SW', 'NW'} and piece.type in {'Bishop', 'Queen'}:
                        return True
                    break  # out of 'while True'. Either own piece, Pawn or Knight so not in check for this direction:
                if king_is_threat:  # King can only attack one square over in each direction
                    king_is_threat = False
        except IndexError:  # Reached end of board
            continue  # to next direction
        return False
                    



DIRECTIONS = 'N NE E SE S SW W NW'.split()

NEXT_MOVE_COORD = { 
    'N': lambda x, y: (x, y + 1),
    'NE': lambda x, y: (x + 1, y + 1),
    'E': lambda x, y: (x + 1, y),
    'SE': lambda x, y: (x + 1, y - 1),
    'S': lambda x, y: (x, y - 1),
    'SW': lambda x, y: (x - 1, y - 1),
    'W': lambda x, y: (x - 1, y),
    'NW': lambda x, y: (x - 1, y + 1)
}
