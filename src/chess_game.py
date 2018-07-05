"""Module for ChessGame class."""
from collections import defaultdict

from src.game_helper import move_direction
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


class ChessGame():
    """Main game logic for chess game.

       Attributes:
            board:  8 * 8 grid (list of lists)
            pieces: dict of defaultdict(int), tracks pieces on board

       Constants:
            MAX_BOARD_WIDTH:  8
            MAX_BOARD_HEIGHT: 8
            MAX_PIECES: dict of max pieces per color; Piecename: max

        Methods:
            add:  add piece to board
            move: move piece from coordinates, to coordinates 
    """
    MAX_BOARD_WIDTH = 8
    MAX_BOARD_HEIGHT = 8
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
            'white': defaultdict(int),
            'black': defaultdict(int)
        }

    def new_game(self):
        # TODO Add functionality to create new board with full set of pieces
        raise NotImplementedError()

    def restore_game(self):
        # TODO Add functionality to restore game at given point in time
        raise NotImplementedError()

    def add(self, piece, coords):
        """Add piece to board at given coordinates. Update piece to have same coordinates.

           Args:
                piece:  Any chess piece devived from GamePiece ABC
                coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1)
        """
        if self._legal_board_position(coords) and not self._max_quantity(piece):
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
        if not self._coords_on_board(from_coords):
            raise NotOnBoardError(from_coords, 'From coordinates not valid board coordinates')

        if not self._coords_on_board(to_coords):
            raise NotOnBoardError(to_coords, 'To coordinates not valid board coordinates')

        piece = self.board[from_coords.x][from_coords.y]
        if not piece:
            raise PieceNotFoundError(from_coords, 'No piece found at from coordinates')

        if from_coords == to_coords:
            raise InvalidMoveError(from_coords, to_coords, 'Move to same square invalid')

        if self._pieces_blocking_move(piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Piece blocking this move')

        if not self._valid_piece_move(piece, to_coords):
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')
        
        # No exceptions raised, safe to move piece
        self._move(piece, to_coords)

    def _move(self, piece, coords):
        """Clear current piece postion, remove captured piece, place piece on new coordinates."""
        # Empty piece current square
        self.board[piece.x_coord][piece.y_coord] = None

        # If move is capture, remove captured piece
        board_postion = self.board[coords.x][coords.y]
        if board_postion is not None:
            captured_piece = board_postion
            captured_piece.x_coord = None
            captured_piece.y_coord = None
            board_postion = None
            self.pieces[captured_piece.color][captured_piece.type] -= 1

        # Place piece at new coordinates
        self._place(piece, coords)

    def _place(self, piece, coords):
        """Add piece to coordinates and update piece coordinates."""
        self.board[coords.x][coords.y] = piece
        piece.x_coord = coords.x
        piece.y_coord = coords.y

    def _coords_on_board(self, coords):
        """Helper method. Return bool"""
        if (coords.x not in range(self.MAX_BOARD_WIDTH) 
                or coords.y not in range(self.MAX_BOARD_HEIGHT)):
            return False
        return True

    def _pieces_blocking_move(self, piece, coords):
        """Helper method. Return bool."""
        if piece.type == 'Knight': # Knight can jump over pieces
            return False

        # Sort coords so logical direction of move not important
        # (x=5, y=6) -> (x=1, y=2) same as (x=1, y=2) -> (x=5, y=6)
        min_x_coord, max_x_coord = sorted([piece.x_coord, coords.x])
        min_y_coord, max_y_coord = sorted([piece.y_coord, coords.y])
        direction = move_direction(piece, coords)

        if direction == 'vertical':
            for next_y_coord in range(min_y_coord + 1, max_y_coord):
                if self.board[piece.x_coord][next_y_coord] is not None:
                    return True
        elif direction == 'horizontal':
            for next_x_coord in range(min_x_coord + 1, max_x_coord):
                if self.board[next_x_coord][piece.y_coord] is not None:
                    return True
        elif direction == 'diagonal':
            next_y_coord = min_y_coord + 1
            for next_x_coord in range(min_x_coord + 1, max_x_coord):
                if self.board[next_x_coord][next_y_coord] is not None:
                    return True
                next_y_coord += 1 

        # No pieces blocking
        return False

    def _valid_piece_move(self, piece, to_coords):
        """Check if to_coords are valid move or capture for piece. Return bool."""
        if self.board[to_coords.x][to_coords.y] is None:  
            # Empty square == move
            return piece.valid_move(to_coords)
        # Occupied square == capture
        return piece.valid_capture(to_coords)

    def _legal_board_position(self, coords):
        """Check passed coordinates are valid. Return bool."""
        try:
            if self.board[coords.x][coords.y] is None:
                return True
            return False
        except IndexError:  # Not on ChessBoard
            return False

    def _max_quantity(self, piece):
        """Check quantity of passed piece on board. Return bool."""
        return self.pieces[piece.color][piece.type] >= self.MAX_PIECES[piece.type]
