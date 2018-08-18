"""Module for ChessGame class."""
from collections import defaultdict

from src.game_enums import Color
from src.game_helper import add, check_coord_errors, Coords
from src.chess_helper import chess_piece_blocking, new_chess_setup
from src.game_errors import InvalidMoveError
from src.chess_helper import king_in_check


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
        self.game_kings = {
            Color.WHITE: {  # TODO Quick fix. None would be preferable for coords but fails tests
                'coords': Coords(x=-99, y=-99),
                'in_check': False
            },
            Color.BLACK: {
                'coords': Coords(x=-99, y=-99),
                'in_check': False
            }
        }
        self.board = [[None] * 8 for _ in range(8)]
        self._setup_board(restore_positions)

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

    def _setup_board(self, game_positions):
        """Setup board for new or previously stored game."""
        if game_positions is None:
            game_positions = new_chess_setup()

        for coords, piece in game_positions.items():
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            add(piece, self, coords)
        
        for row in self.board:  # TODO Quick and dirty fix, better way?
            for piece in row:
                if piece and piece.type == 'King':
                    self.game_kings[piece.color]['coords'] = piece.coords

                    opponent_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK
                    if king_in_check(piece.coords, self.board, opponent_color):
                        self.game_kings[piece.color]['in_check'] = True

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
            self.game_kings[piece.color]['coords'] = piece.coords

        # Check if oppenent put in check
        opponent_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK
        king_coords = self.game_kings[opponent_color]['coords']
        if king_in_check(king_coords, self.board, piece.color):
            self.game_kings[opponent_color]['in_check'] = True

        # Un-flag own king from being in check (if applicable)
        if self.game_kings[piece.color]['in_check']:
            self.game_kings[piece.color]['in_check'] = False

    def _move_errors(self, board, from_coords, to_coords):
        """Helper function for move. Raise errors or return False."""
        check_coord_errors(board, from_coords, to_coords)

        if chess_piece_blocking(board, from_coords, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Piece blocking this move')

        piece = self.board[from_coords.x][from_coords.y]

        if not self._valid_piece_move(piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')

        if self._own_king_in_check(board, piece, to_coords):
            # Covers both: move putting own king in check, not moving king out of check from previous move
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move, king is in check')

        return False

    def _valid_piece_move(self, piece, to_coords):
        """Check if to_coords are valid move or capture for piece. Return bool."""
        if self.board[to_coords.x][to_coords.y] is None:
            return piece.valid_move(to_coords)  # Empty square == move
        return piece.valid_capture(to_coords)   # Occupied square == capture

    def _own_king_in_check(self, board, piece, to_coords):
        # Keep track of current game state
        original_piece = board[to_coords.x][to_coords.y]
        original_king_coords = self.game_kings[piece.color]['coords']
        opponent_color = Color.WHITE if piece.color == Color.BLACK else Color.BLACK

        # Temporarily change to future board position to see if it will lead to check
        board[piece.coords.x][piece.coords.y] = None
        board[to_coords.x][to_coords.y] = piece
        if piece.type == 'King':
            self.game_kings[piece.color]['coords'] = to_coords

        # Perform check
        king_coords = self.game_kings[piece.color]['coords']
        in_check = True if king_in_check(king_coords, board, opponent_color) else False

        # Return game to previous state
        board[piece.coords.x][piece.coords.y] = piece
        board[to_coords.x][to_coords.y] = original_piece
        self.game_kings[piece.color]['coords'] = original_king_coords

        return in_check
