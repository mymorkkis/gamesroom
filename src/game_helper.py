"""Module of helper functions for games.

   Object:
        Coords: namedtuple('Coords', 'x y').

   Functions:
        move_direction: Return move direction as Direction enum type.
        legal_start_position: Check passed start coordinates are valid.
        coord_errors: Check for errors in passed board coordinates.
        coords_on_board: Check coordinates are on board.
        chess_piece_blocking: Check if piece blocking chess game move.
"""
from collections import namedtuple

from src.game_enums import Direction
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


Coords = namedtuple('Coords', 'x y')


def add(piece, board, coords, pieces):
    """Add piece on board at given coordinates and update piece coordinates. Increment pieces.

       Raises:
            NotOnBoardError
    """
    # TODO Error if wrong piece color / piece type
    try:
        board[coords.x][coords.y] = piece
        piece.coords = coords
        pieces[piece.color][piece.type] += 1
    except IndexError:
        raise NotOnBoardError(coords, 'Saved coordinates are not valid coordinates')


def move_direction(from_coords, to_coords):
    """Calculate direction from from_coordinates to coordinates. Return Direction enum.

       Args:
            from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
            to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).

       Returns:
            Direction enum type.
    """
    if abs(from_coords.x - to_coords.x) == abs(from_coords.y - to_coords.y):
        return Direction.DIAGONAL
    elif from_coords.x != to_coords.x and from_coords.y == to_coords.y:
        return Direction.HORIZONTAL
    elif from_coords.y != to_coords.y and from_coords.x == to_coords.x:
        return Direction.VERTICAL
    else:
        return Direction.NON_LINEAR


def check_coord_errors(piece, board, from_coords, to_coords):
    """Check for errors in passed board coordinates.

       Args:
            piece:       Game piece found at from_coords.
            board:       Game board.
            from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
            to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).

       Raises:
            NotOnBoardError:    If either passed coordinates are not in board grid.
            InvalidMoveError:   If from_coords and to_coords are the same.
            PieceNotFoundError: If no piece found at from coordinates.

    """
    if not coords_on_board(board, from_coords):
        raise NotOnBoardError(from_coords, 'From coordinates not valid board coordinates')

    if not coords_on_board(board, to_coords):
        raise NotOnBoardError(to_coords, 'To coordinates not valid board coordinates')

    if from_coords == to_coords:
        raise InvalidMoveError(from_coords, to_coords, 'Move to same square invalid')

    if not piece:
        raise PieceNotFoundError(from_coords, 'No piece found at from coordinates')


def coords_on_board(board, coords):
    """Check if coordinates within board range. Return bool."""
    return coords.x < len(board) and coords.y < len(board)
