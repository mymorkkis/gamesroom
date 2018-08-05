"""Module for ChessGame class."""
from collections import defaultdict

from src.game_enums import Color
from src.game_helper import add, chess_piece_blocking, check_coord_errors, Coords
from src.game_setup import new_chess_setup
from src.game_errors import InvalidMoveError


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
        self.board = self._setup_board(restore_positions)

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
        piece = self.board[from_coords.x][from_coords.y]

        if not self._move_errors(piece, self.board, from_coords, to_coords):
            self._move(piece, from_coords, to_coords)

    def _setup_board(self, game_positions):
        """Setup board for new or previously stored game."""
        board = [[None] * 8 for _ in range(8)]

        if game_positions is None:
            game_positions = new_chess_setup()

        for coords, piece in game_positions.items():
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            add(piece, board, coords, self.pieces)

        return board   
        
    def _move(self, piece, from_coords, to_coords):
        # Remove piece from current coordinates
        self.board[from_coords.x][from_coords.y] = None

        # If move is capture, remove captured piece
        board_postion = self.board[to_coords.x][to_coords.y]
        if board_postion is not None:
            captured_piece = board_postion
            captured_piece.x_coord = None
            captured_piece.y_coord = None
            board_postion = None
            self.pieces[captured_piece.color][captured_piece.type] -= 1

        # add piece at new coordinates
        self.board[to_coords.x][to_coords.y] = piece
        piece.x_coord = to_coords.x
        piece.y_coord = to_coords.y


    def _move_errors(self, piece, board, from_coords, to_coords):
        """Helper function for move. Raise errors or return False."""
        check_coord_errors(piece, board, from_coords, to_coords)

        if chess_piece_blocking(board, from_coords, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Piece blocking this move')
        
        if not self._valid_piece_move(piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')

        return False

    def _valid_piece_move(self, piece, to_coords):
        """Check if to_coords are valid move or capture for piece. Return bool."""
        if self.board[to_coords.x][to_coords.y] is None:
            return piece.valid_move(to_coords)  # Empty square == move
        return piece.valid_capture(to_coords)   # Occupied square == capture
