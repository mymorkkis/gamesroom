"""Module for ChessGame class."""
from collections import defaultdict

from src.game_enums import Color
from src.game_helper import add, check_coord_errors, Coords
from src.game_errors import InvalidMoveError
from src.chess_helper import (castle_attempt, chess_piece_blocking, valid_castle, king_in_check,
                              new_chess_setup, own_king_in_check, VALID_PIECE_TYPES)


class ChessGame():
    """Main game logic for chess game.

       Optional Argument:
            restore_positions:
                dict of pieces for game restore
                expected in the following key/value format:
                key = str representation of game coordinates xy
                value = chess GamePiece
                e.g. "32": Queen.WHITE
                White Queen will be placed at Coords(x=3, y=2)

       Attributes:
            board:  8 * 8 grid (list of lists)
            pieces: dict of defaultdict(int), tracks pieces on board

       Methods:
            move: move piece from coordinates, to coordinates
    """
    def __init__(self, restore_positions=None):
        self.pieces = {
            Color.WHITE: defaultdict(int),
            Color.BLACK: defaultdict(int)
        }
        self.king_coords = {
            Color.WHITE: None,
            Color.BLACK: None
        }
        self.board = [[None] * 8 for _ in range(8)]
        self._setup_game(restore_positions)

    def move(self, from_coords, to_coords):
        """Move piece from coordinates, to coordianates. Remove captured piece, if any.

           Args:
                from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
                to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).

           Raises:
                NotOnBoardError:    If either passed coordinates are not in board grid.
                PieceNotFoundError: If no piece found at from coordinates.
                InvalidMoveError:   If attempted move not in-line with game rules.
        """
        if not self._move_errors(self.board, from_coords, to_coords):
            piece = self.board[from_coords.x][from_coords.y]
            self._move(piece, from_coords, to_coords)

    def _setup_game(self, game_positions):
        """Setup board for new or previously stored game."""
        if game_positions is None:
            game_positions = new_chess_setup()

        for coords, piece in game_positions.items():
            assert isinstance(piece.color, Color)
            assert piece.type in VALID_PIECE_TYPES
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            add(piece, self, coords)

    def _move(self, piece, from_coords, to_coords):
        # Remove piece from current coordinates
        self.board[from_coords.x][from_coords.y] = None

        # If move is capture, remove captured piece
        board_postion = self.board[to_coords.x][to_coords.y]
        if board_postion is not None:
            captured_piece = board_postion
            captured_piece.coords = None
            board_postion = None
            self.pieces[captured_piece.color][captured_piece.type] -= 1

        # Add piece at new coordinates
        self.board[to_coords.x][to_coords.y] = piece
        piece.coords = to_coords
        if piece.type == 'King':
            self.king_coords[piece.color] = piece.coords

        # Mark if King or Rook moved to disallow later castling
        if piece.type in ('King', 'Rook') and not piece.moved:
            piece.moved = True

        # Check if oppenent put in check
        opponent_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK
        king_coords = self.king_coords[opponent_color]
        if king_in_check(king_coords, self.board, piece.color):
            opponent_king = self.board[king_coords.x][king_coords.y]
            opponent_king.in_check = True

        # Un-flag own king from being in check (if applicable)
        king_coords = self.king_coords[piece.color]
        king = self.board[king_coords.x][king_coords.y]
        if king.in_check:
            king.in_check = False

    def _move_errors(self, board, from_coords, to_coords):
        """Helper function for move. Raise errors or return False."""
        check_coord_errors(board, from_coords, to_coords)

        if chess_piece_blocking(board, from_coords, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Piece blocking this move')

        piece = self.board[from_coords.x][from_coords.y]

        if not self._valid_piece_move(piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')

        if own_king_in_check(self, piece, to_coords):
            # Covers both: move putting own king in check, not moving king out of check from previous move
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move, king is in check')

        if castle_attempt(piece, to_coords) and not valid_castle(self.board, piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Invalid castle') # TODO Add reason

        return False

    def _valid_piece_move(self, piece, to_coords):
        """Check if to_coords are valid move or capture for piece. Return bool."""
        if self.board[to_coords.x][to_coords.y] is None:
            return piece.valid_move(to_coords)  # Empty square == move
        return piece.valid_capture(to_coords)   # Occupied square == capture
