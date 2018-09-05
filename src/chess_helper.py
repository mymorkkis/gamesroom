"""Helper functions for ChessGame.

   Constants:
        VALID_PIECE_TYPES:      Set of valid chess piece types as str.

   Functions:
        new_chess_setup:        Return dict of chess start positions. position: piece
        chess_piece_blocking:   Check if piece blocking move. Return bool.
        castling:               Check if castle attempt being made. Return bool.
        valid_castle:           Validate attempted castle move. Return bool.
        move_rook:              Move Rook to other side of King during castle.
        own_king_in_check:      Check if move puts current player king in check. Return bool.
        king_in_check:          Check for King being put into check. Return bool.
"""
from src.game_enums import Color
from src.game_enums import Direction
from src.game_helper import Coords, coords_on_board, move_direction, opponent_color_

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


VALID_PIECE_NAMES = {'Bishop', 'King', 'Knight', 'Pawn', 'Queen', 'Rook'}

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
        for x_coord, y_coord in _diagonal_coords(from_coords, to_coords):
            if board[x_coord][y_coord] is not None:
                return True
    else:  # Should never reach here
        raise ValueError('Invalid direction in chess_piece_blocking func')

    return False  # No piece blocking

def _diagonal_coords(from_coords, to_coords):
    """Helper function for chess_piece_blocking. Return zip of all diagonal coords."""
    if from_coords.x > to_coords.x:
        x_coords = reversed(list(range(to_coords.x + 1, from_coords.x)))
    else:
        x_coords = list(range(from_coords.x + 1, to_coords.x))

    if from_coords.y > to_coords.y:
        y_coords = reversed(list(range(to_coords.y + 1, from_coords.y)))
    else:
        y_coords = list(range(from_coords.y + 1, to_coords.y))

    return zip(x_coords, y_coords)

def castling(piece, to_coords):
    """Check if castle attempt being made. Return bool."""
    if piece.name == 'King' and piece.coords == Coords(x=4, y=0):
        return to_coords in (Coords(x=2, y=0), Coords(x=6, y=0))
    if piece.name == 'King' and piece.coords == Coords(x=4, y=7):
        return to_coords in (Coords(x=2, y=7), Coords(x=6, y=7))
    return False


def valid_castle(board, king, to_coords):
    """Validate attempted castle move. Return bool."""
    if king.in_check:
        return False

    if king.coords == Coords(x=4, y=0) and to_coords == Coords(x=2, y=0):
        potential_rook = board[0][0]
        king_move_coords = (Coords(x=3, y=0), Coords(x=2, y=0))
        return _valid_castle(board, king, king_move_coords, potential_rook, opponent_color_(king))

    if king.coords == Coords(x=4, y=0) and to_coords == Coords(x=6, y=0):
        potential_rook = board[7][0]
        king_move_coords = (Coords(x=5, y=0), Coords(x=6, y=0))
        return _valid_castle(board, king, king_move_coords, potential_rook, opponent_color_(king))

    if king.coords == Coords(x=4, y=7) and to_coords == Coords(x=2, y=7):
        potential_rook = board[0][7]
        king_move_coords = (Coords(x=3, y=7), Coords(x=2, y=7))
        return _valid_castle(board, king, king_move_coords, potential_rook, opponent_color_(king))

    if king.coords == Coords(x=4, y=0) and to_coords == Coords(x=6, y=7):
        potential_rook = board[7][7]
        king_move_coords = (Coords(x=5, y=7), Coords(x=6, y=7))
        return _valid_castle(board, king, king_move_coords, potential_rook, opponent_color_(king))

    return True


def _valid_castle(board, king, king_move_coords, potential_rook, opponent_color):
    """Helper function. Main logic for valid castle. Return bool."""
    if potential_rook and potential_rook.name == 'Rook':
        rook = potential_rook
        thru, to = king_move_coords
        move_thru, move_to = board[thru.x][thru.y], board[to.x][to.y]

        if king.moved or rook.moved:
            return False
        if move_thru or move_to:  # Piece blocking castle
            return False
        for coord in king_move_coords:
            if king_in_check(coord, board, opponent_color):
                return False
        return True
    return False  # No Rook to castle


def move_rook(board, king_coords):
    """Part of castle move. Move Rook to other side of King."""
    if king_coords == Coords(x=6, y=0):
        rook = board[7][0]
        board[7][0] = None
        board[5][0] = rook
        rook.coords = Coords(x=5, y=0)
    if king_coords == Coords(x=2, y=0):
        rook = board[0][0]
        board[0][0] = None
        board[3][0] = rook
        rook.coords = Coords(x=3, y=0)
    if king_coords == Coords(x=6, y=7):
        rook = board[7][7]
        board[7][7] = None
        board[5][7] = rook
        rook.coords = Coords(x=5, y=7)
    if king_coords == Coords(x=2, y=7):
        rook = board[0][7]
        board[0][7] = None
        board[3][7] = rook
        rook.coords = Coords(x=3, y=7)


def own_king_in_check(game, piece, to_coords):
    """Check if move puts current player king in check. Return bool."""
    # Keep track of current game state
    original_piece = game.board[to_coords.x][to_coords.y]
    original_king_coords = game.king_coords[piece.color]

    # Temporarily change to future board position to see if it will lead to check
    game.board[piece.coords.x][piece.coords.y] = None
    game.board[to_coords.x][to_coords.y] = piece
    if piece.name == 'King':
        game.king_coords[piece.color] = to_coords

    # Perform check evaluation
    king_coords = game.king_coords[piece.color]
    in_check = True if king_in_check(king_coords, game.board, opponent_color_(piece)) else False

    # Return game to previous state
    game.board[piece.coords.x][piece.coords.y] = piece
    game.board[to_coords.x][to_coords.y] = original_piece
    game.king_coords[piece.color] = original_king_coords

    return in_check


def king_in_check(king_coords, board, opponent_color):
    """Check all 8 board directions to see if king is in check. Return bool."""
    if _pawn_check(king_coords, board, opponent_color):
        return True
    if _knight_check(king_coords, board, opponent_color):
        return True
    if _check_by_other_piece(king_coords, board, opponent_color):
        return True
    return False  # King not in check


def _pawn_check(king_coords, board, opponent_color):
    """Helper function for king_in_check function."""
    pawn = Pawn(opponent_color)
    if opponent_color == Color.WHITE:
        x, y = king_coords.x + 1, king_coords.y - 1
        if coords_on_board(board, x, y) and board[x][y] == pawn:
            return True
        x, y = king_coords.x - 1, king_coords.y - 1
        if coords_on_board(board, x, y) and board[x][y] == pawn:
            return True
    if opponent_color == Color.BLACK:
        x, y = king_coords.x + 1, king_coords.y + 1
        if coords_on_board(board, x, y) and board[x][y] == pawn:
            return True
        x, y = king_coords.x - 1, king_coords.y + 1
        if coords_on_board(board, x, y) and board[x][y] == pawn:
            return True
    return False


def _knight_check(king_coords, board, opponent_color):
    """Helper function for king_in_check function."""
    test_coords = [
        (king_coords.x + 1, king_coords.y + 2),
        (king_coords.x + 1, king_coords.y - 2),
        (king_coords.x + 2, king_coords.y + 1),
        (king_coords.x + 2, king_coords.y - 1),
        (king_coords.x - 1, king_coords.y + 2),
        (king_coords.x - 1, king_coords.y - 2),
        (king_coords.x - 2, king_coords.y + 1),
        (king_coords.x - 2, king_coords.y - 1),
    ]
    for coord in test_coords:
        x, y = coord[0], coord[1]
        if coords_on_board(board, x, y) and board[x][y] == Knight(opponent_color):
            return True
    return False


def _check_by_other_piece(king_coords, board, opponent_color):
    """Helper function for king_in_check function."""
    for direction in 'N NE E SE S SW W NW'.split():
        next_x, next_y = king_coords
        king_is_threat = True
        while True:
            next_x, next_y = _next_move_coord[direction](next_x, next_y)
            if not coords_on_board(board, next_x, next_y):
                break
            piece = board[next_x][next_y]
            if piece and piece.color != opponent_color:
                break  # Own piece blocking possible check from this direction
            if piece and piece.color == opponent_color:
                if piece.name == 'King' and king_is_threat:
                    return True
                elif direction in {'N', 'E', 'S', 'W'} and piece.name in {'Rook', 'Queen'}:
                    return True
                elif direction in {'NE', 'SE', 'SW', 'NW'} and piece.name in {'Bishop', 'Queen'}:
                    return True
                break  # Either Pawn or Knight so not in check for this direction:
            if king_is_threat:
                king_is_threat = False  # King can only attack one square over in each direction
    return False

# def check_mate(king, attacking_piece, board):
#     if not _king_cant_move(king, board, piece.color):
#         return False


def king_cant_move(king, board, opponent_color):
    """Check if king can move to any square without being in check. Return bool."""
    for direction in 'N NE E SE S SW W NW'.split():
        next_x, next_y = _next_move_coord[direction](king.coords.x, king.coords.y)
        if not coords_on_board(board, next_x, next_y):
            continue
        king_border_square = board[next_x][next_y]
        test_king_coords = Coords(x=next_x, y=next_y)
        if (king_border_square is None
                and not king_in_check(test_king_coords, board, opponent_color)):
            return False
    return True


_next_move_coord = {
    'N': lambda x, y: (x, y + 1),
    'NE': lambda x, y: (x + 1, y + 1),
    'E': lambda x, y: (x + 1, y),
    'SE': lambda x, y: (x + 1, y - 1),
    'S': lambda x, y: (x, y - 1),
    'SW': lambda x, y: (x - 1, y - 1),
    'W': lambda x, y: (x - 1, y),
    'NW': lambda x, y: (x - 1, y + 1)
}
