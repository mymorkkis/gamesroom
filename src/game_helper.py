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

def piece_blocking(board, from_coords, to_coords):
    """Helper method. Return bool."""
    # Sort coords so logical direction of move not important
    # (x=5, y=6) -> (x=1, y=2) same as (x=1, y=2) -> (x=5, y=6)
    min_x_coord, max_x_coord = sorted([from_coords.x, to_coords.x])
    min_y_coord, max_y_coord = sorted([from_coords.y, to_coords.y])
    direction = move_direction(from_coords, to_coords)

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
