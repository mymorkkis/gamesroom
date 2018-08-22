"""Helper functions for ChessGame."""
from src.game_enums import Color
from src.game_enums import Direction
from src.game_helper import coords_on_board, move_direction

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


VALID_PIECE_TYPES = {'King', 'Queen', 'Rook', 'Bishop', 'Knight', 'Pawn'}


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


def own_king_in_check(game, piece, to_coords):
    """Check if move puts current player king in check. Return bool."""
    # Keep track of current game state
    original_piece = game.board[to_coords.x][to_coords.y]
    original_king_coords = game.king_coords[piece.color]
    opponent_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK

    # Temporarily change to future board position to see if it will lead to check
    game.board[piece.coords.x][piece.coords.y] = None
    game.board[to_coords.x][to_coords.y] = piece
    if piece.type == 'King':
        game.king_coords[piece.color] = to_coords

    # Perform check evaluation
    king_coords = game.king_coords[piece.color]
    in_check = True if king_in_check(king_coords, game.board, opponent_color) else False

    # Return game to previous state
    game.board[piece.coords.x][piece.coords.y] = piece
    game.board[to_coords.x][to_coords.y] = original_piece
    game.king_coords[piece.color] = original_king_coords

    return in_check


def king_in_check(king_coords, board, opponent_color):
    """Check all 8 directions for king being in check. Return bool."""
    if _pawn_check(king_coords, board, opponent_color):
        return True
    if _knight_check(king_coords, board, opponent_color):
        return True
    if _check_by_other_piece(king_coords, board, opponent_color):
        return True
    return False  # King not in check


def _pawn_check(king_coords, board, opponent_color):
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
    for direction in 'N NE E SE S SW W NW'.split():
        next_x, next_y = king_coords
        king_is_threat = True
        while True:
            next_x, next_y = NEXT_MOVE_COORD[direction](next_x, next_y)
            if not coords_on_board(board, next_x, next_y):
                break
            piece = board[next_x][next_y]
            if piece and piece.color != opponent_color:
                break  # Own piece blocking possible check from this direction
            if piece and piece.color == opponent_color:
                if piece.type == 'King' and king_is_threat:
                    return True
                elif direction in {'N', 'E', 'S', 'W'} and piece.type in {'Rook', 'Queen'}:
                    return True
                elif direction in {'NE', 'SE', 'SW', 'NW'} and piece.type in {'Bishop', 'Queen'}:
                    return True
                break  # Either Pawn or Knight so not in check for this direction:
            if king_is_threat:
                king_is_threat = False  # King can only attack one square over in each direction
    return False


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
