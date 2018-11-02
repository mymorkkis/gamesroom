from abc import ABC, abstractmethod
from collections import namedtuple

from src.game_enums import Direction
from src.game_errors import IllegalMoveError, NotOnBoardError, PieceNotFoundError


Coords = namedtuple('Coords', 'x y')


class Game(ABC):
    def __init__(self, board, legal_piece_colors, legal_piece_names,
                 pieces, restore_positions):
        self.board = board
        self.board_width = len(self.board[0])
        self.board_height = len(self.board)
        self.pieces = pieces
        self.legal_piece_names = legal_piece_names
        self.legal_piece_colors = legal_piece_colors
        self._setup_game(restore_positions)
        self.winner = None
        # Move attributes
        self.from_coords = None
        self.to_coords = None
        self.playing_piece = None

    @abstractmethod
    def move(self, from_coords, to_coords):
        raise NotImplementedError

    @abstractmethod
    def new_setup(self):
        raise NotImplementedError

    def _setup_game(self, game_positions):
        """Setup board for new or previously stored game."""
        if game_positions is None:
            game_positions = self.new_setup()

        for coords, piece in game_positions.items():
            assert piece.color in self.legal_piece_colors
            assert piece.name in self.legal_piece_names
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            self.add(piece, coords)

    def save_game(self):
        pass

    def add(self, piece, coords):
        """Add piece on board at given coordinates and update piece coordinates. Increment pieces.
        (Chess only): Add King coordinates to king_coords dictionary.
        Args:
                piece:  Any piece that inherits from GamePiece
                game:   Game object
                coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
        Raises:
                NotOnBoardError
        """
        try:
            self.board[coords.x][coords.y] = piece
            piece.coords = coords
            self.pieces[piece.color][piece.name] += 1
        except IndexError:
            raise NotOnBoardError(coords, 'Saved coordinates are not legal coordinates')

    def set_move_attributes(self, from_coords, to_coords, playing_color):
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.playing_piece = self.board[from_coords.x][from_coords.y]
        if self.playing_piece.color != playing_color:
            raise IllegalMoveError(from_coords, to_coords, 'Incorrect piece color for current player')

    def coords_on_board(self, x_coord, y_coord):
        """Check if coordinates within board range (negative indexing not allowed). Return bool."""
        return x_coord in range(self.board_width) and y_coord in range(self.board_height)

    def validate_coords(self, from_coords, to_coords):
        """Check for errors in passed board coordinates.
        Args:
                board:       Game board.
                from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
                to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
        Raises:
                NotOnBoardError:    If either passed coordinates are not in board grid.
                IllegalMoveError:   If from_coords and to_coords are the same.
                PieceNotFoundError: If no piece found at from coordinates.
        """
        if not self.coords_on_board(from_coords.x, from_coords.y):
            raise NotOnBoardError(from_coords, 'From coordinates not board coordinates')

        if not self.coords_on_board(to_coords.x, to_coords.y):
            raise NotOnBoardError(to_coords, 'To coordinates not board coordinates')

        if from_coords == to_coords:
            raise IllegalMoveError(from_coords, to_coords, 'Move to same square illegal')

        piece = self.board[from_coords.x][from_coords.y]
        if not piece:
            raise PieceNotFoundError(from_coords, 'No piece found at from coordinates')

    def coords_between(self, from_coords, to_coords):
        """Helper function. Return generator of all coords between from_coords and to_coords."""
        x_coords = self._x_coords(from_coords, to_coords)
        y_coords = self._y_coords(from_coords, to_coords)
        return (Coords(x, y) for x, y in zip(x_coords, y_coords))

    def _y_coords(self, from_coords, to_coords):
        if from_coords.y > to_coords.y:
            y_coords = reversed(list(range(to_coords.y + 1, from_coords.y)))
        elif from_coords.y == to_coords.y:
            list_length = abs(from_coords.x - to_coords.x)
            y_coords = list_length * [from_coords.y]
        else:
            y_coords = list(range(from_coords.y + 1, to_coords.y))
        return y_coords

    def _x_coords(self, from_coords, to_coords):
        if from_coords.x > to_coords.x:
            x_coords = reversed(list(range(to_coords.x + 1, from_coords.x)))
        elif from_coords.x == to_coords.x:
            list_length = abs(from_coords.y - to_coords.y)
            x_coords = list_length * [from_coords.x]
        else:
            x_coords = list(range(from_coords.x + 1, to_coords.x))
        return x_coords


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


def adjacent_squares(from_coords, to_coords):
    """Check if to_coordinates are adjacent to from_coordinates. Return bool."""
    x_abs = abs(from_coords.x - to_coords.x)
    y_abs = abs(from_coords.y - to_coords.y)
    if x_abs == 0 or y_abs == 0:
        return x_abs + y_abs == 1
    return x_abs + y_abs == 2
