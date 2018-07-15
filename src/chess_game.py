"""Module for ChessGame class."""
from collections import defaultdict

from src.game_enums import Color
from src.game_errors import InvalidMoveError, NotOnBoardError
from src.game_helper import (chess_piece_blocking, check_coord_errors, 
                             Coords, legal_start_position)
from src.game_setup import new_chess_setup


class ChessGame():
    """Main game logic for chess game.

       Attributes:
            board:  8 * 8 grid (list of lists)
            pieces: dict of defaultdict(int), tracks pieces on board

       Constants:
            MAX_PIECES: dict of max pieces per color; Piecename: max

       Methods:
            add:  add piece to board
            move: move piece from coordinates, to coordinates 
    """
    MAX_PIECES = {
        'Pawn': 8,
        'Knight': 2,
        'Bishop': 2,
        'Rook': 2,
        'Queen': 1,
        'King': 1
    }

    def __init__(self):
        self.board = [[None] * 8 for _ in range(8)]
        # TODO Handle Pawn promoting to an extra Queen etc
        self.pieces = {
            Color.WHITE: defaultdict(int),
            Color.BLACK: defaultdict(int)
        }

    def setup_board(self, setup=None):
        """Setup board for new or previously stored game.
           
           Optional Args:
                setup: dict of pieces for game restore. 

           Setup dict expected in the following key/value format:
                key = str representation of game coordinates xy
                value = chess GamePiece
                e.g. "32": Queen.WHITE
                White Queen will be placed at Coords(x=3, y=2)
        """
        if setup is None:
            setup = new_chess_setup()

        for coord, piece in setup.items():
            try:
                coords = Coords(x=int(coord[0]), y=int(coord[1]))
                self._place(piece, coords)
                self.pieces[piece.color][piece.type] += 1
            except IndexError:
                raise NotOnBoardError(coords, 'Saved coordinates are not valid coordinates')          

    def add(self, piece, coords):
        """Add piece to board at given coordinates. Update piece to have same coordinates.

           Args:
                piece:  Any chess piece devived from GamePiece ABC
                coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)
        """
        if legal_start_position(self.board, coords) and not self._max_quantity(piece):
            self.pieces[piece.color][piece.type] += 1
            self._place(piece, coords)

    def move(self, from_coords, to_coords):
        """Move piece from coordinates, to coordianates. Remove captured piece, if any.

           Args:
                from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)
                to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)

           Raises:
                NotOnBoardError:    If either passed coordinates are not in board grid.
                PieceNotFoundError: If no piece found at from coordinates.
                InvalidMoveError:   If attempted move not in-line with game rules.
        """
        piece = self.board[from_coords.x][from_coords.y]

        if not self._move_errors(piece, self.board, from_coords, to_coords):
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

            # Place piece at new coordinates
            self._place(piece, to_coords)

    def _place(self, piece, coords):
        """Add piece to coordinates and update piece coordinates."""
        self.board[coords.x][coords.y] = piece
        piece.x_coord = coords.x
        piece.y_coord = coords.y

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

    def _max_quantity(self, piece):
        """Check quantity of passed piece on board. Return bool."""
        return self.pieces[piece.color][piece.type] >= self.MAX_PIECES[piece.type]
