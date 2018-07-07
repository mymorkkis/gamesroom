"""Module for ChessGame class."""
from collections import defaultdict, namedtuple

from src.game_enums import Color, Direction
from src.game_errors import InvalidMoveError
from src.game_helper import legal_start_position, move_direction, move_errors


Coords = namedtuple('Coords', 'x y')


class ChessGame():
    """Main game logic for chess game.

       Attributes:
            board:  8 * 8 grid (list of lists)
            pieces: dict of defaultdict(int), tracks pieces on board

       Constants:
            BOARD_WIDTH:  8
            BOARD_HEIGHT: 8
            MAX_PIECES: dict of max pieces per color; Piecename: max

        Methods:
            add:  add piece to board
            move: move piece from coordinates, to coordinates 
    """
    BOARD_WIDTH = 8
    BOARD_HEIGHT = 8
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

        if (not move_errors(piece, from_coords, to_coords, self.BOARD_WIDTH, self.BOARD_HEIGHT)
                and not self._piece_blocking_move(piece, to_coords) 
                and self._valid_piece_move(piece, to_coords)):
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

    def _piece_blocking_move(self, piece, to_coords):
        """Helper method. Return bool."""
        from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
        if piece.type == 'Knight' or not self._piece_blocking(piece, from_coords, to_coords):
            return False
        raise InvalidMoveError(from_coords, to_coords, 'Piece blocking this move')

    def _piece_blocking(self, piece, from_coords, to_coords):
        # Sort coords so logical direction of move not important
        # (x=5, y=6) -> (x=1, y=2) same as (x=1, y=2) -> (x=5, y=6)
        min_x_coord, max_x_coord = sorted([piece.x_coord, to_coords.x])
        min_y_coord, max_y_coord = sorted([piece.y_coord, to_coords.y])
        direction = move_direction(piece, to_coords)

        if direction == Direction.VERTICAL:
            for next_y_coord in range(min_y_coord + 1, max_y_coord):
                if self.board[piece.x_coord][next_y_coord] is not None:
                    return True
        elif direction == Direction.HORIZONTAL:
            for next_x_coord in range(min_x_coord + 1, max_x_coord):
                if self.board[next_x_coord][piece.y_coord] is not None:
                    return True
        elif direction == Direction.DIAGONAL:
            next_y_coord = min_y_coord + 1
            for next_x_coord in range(min_x_coord + 1, max_x_coord):
                if self.board[next_x_coord][next_y_coord] is not None:
                    return True
                next_y_coord += 1 
        else:  # Should never reach here
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')
            
        return False  # No piece blocking

    def _valid_piece_move(self, piece, to_coords):
        """Check if to_coords are valid move or capture for piece. Return bool."""
        if self.board[to_coords.x][to_coords.y] is None:  
            # Empty square == move
            valid = piece.valid_move(to_coords)
        else:  # Occupied square == capture
            valid = piece.valid_capture(to_coords)

        if not valid:
            from_coords = Coords(x=piece.x_coord, y=piece.y_coord)
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')

        return True

    def _max_quantity(self, piece):
        """Check quantity of passed piece on board. Return bool."""
        return self.pieces[piece.color][piece.type] >= self.MAX_PIECES[piece.type]
