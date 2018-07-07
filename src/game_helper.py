"""Module of helper functions for chess game.

   Functions:
        move_direction: Return str representation of move direction.
"""
from src.game_enums import Direction
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError

def move_direction(piece, to_coords):
    """Calculate direction from piece to coordinates. Return Direction enum."""
    if _diagonal_movement(piece, to_coords):
        return Direction.DIAGONAL
    elif piece.x_coord != to_coords.x and piece.y_coord == to_coords.y:
        return Direction.HORIZONTAL
    elif piece.y_coord != to_coords.y and piece.x_coord == to_coords.x:
        return Direction.VERTICAL
    else:
        return Direction.NON_LINEAR


def _diagonal_movement(piece, coords):
    """Helper function for move_direction. Return bool."""
    min_x_coord, max_x_coord = sorted([piece.x_coord, coords.x])
    min_y_coord, max_y_coord = sorted([piece.y_coord, coords.y])
    # Only diagonal if distance equal lengths
    return (max_x_coord - min_x_coord) == (max_y_coord - min_y_coord)


def move_errors(piece, from_coords, to_coords, board_width, board_hight):
    """Helper function for move. Raise errors or return False."""
    if not coords_on_board(from_coords, board_width, board_hight):
        raise NotOnBoardError(from_coords, 'From coordinates not valid board coordinates')

    if not coords_on_board(to_coords, board_width, board_hight):
        raise NotOnBoardError(to_coords, 'To coordinates not valid board coordinates')

    if from_coords == to_coords:
        raise InvalidMoveError(from_coords, to_coords, 'Move to same square invalid')

    if not piece:
        raise PieceNotFoundError(from_coords, 'No piece found at from coordinates')

    return False


def coords_on_board(coords, board_width, board_hight):
    """Check if coordinates withing board range. Return bool"""
    if coords.x not in range(board_width) or coords.y not in range(board_hight):
        return False
    return True


def legal_start_position(board, coords):
    """Check passed coordinates are valid. Return bool or raise NotOnBoardError."""
    try:
        if board[coords.x][coords.y] is None:
            return True
        return False
    except IndexError:
        raise NotOnBoardError(coords, 'Start coordingates not on board')
