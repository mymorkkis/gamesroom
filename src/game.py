"""Main game module with Game abstract base class.

   Functions:
        move_direction:   return move Direction enum type
        adjacent_squares: return bool
"""
from abc import ABC, abstractmethod
from collections import namedtuple

from tabulate import tabulate

from src.game_enums import Direction
from src.game_errors import IllegalMoveError, NotOnBoardError


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

Coords = namedtuple('Coords', 'x y')


class Game(ABC):
    """Abstract Base class for game.

       Methods:
            validate_coords
            add
            set_move_attributes
            coords_on_board
            coords_between
            display_board

       Abstract methods:
            move
            new_setup
    """
    def __init__(self, board, legal_piece_colors, legal_piece_names, restore_positions):
        self.board = board
        self.board_width = len(self.board[0])
        self.board_height = len(self.board)
        self.y_axis = list(reversed(range(self.board_height + 1)))
        self.x_axis = list(ALPHABET[:self.board_width])
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
        'TODO'
        pass

    def add(self, piece, coords):
        """Add piece on board at given coordinates and update piece coordinates.
        Args:
                piece:  Any piece that inherits from GamePiece
                coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
        Raises:
                NotOnBoardError
        """
        try:
            self.board[coords.x][coords.y] = piece
            piece.coords = coords
        except IndexError:
            raise NotOnBoardError(coords, 'Saved coordinates are not legal coordinates')

    def set_move_attributes(self, from_coords, to_coords, playing_color):
        """Sets temporary game attributes, from_coords, to_coords and playing_piece.

           Raises:
                IllegalMoveError
        """
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.playing_piece = self.board[from_coords.x][from_coords.y]
        if self.playing_piece.color != playing_color:
            raise IllegalMoveError('Incorrect piece color for current player')

    def coords_on_board(self, x_coord, y_coord):
        """Check if coordinates within board range (negative indexing not allowed). Return bool."""
        return x_coord in range(self.board_width) and y_coord in range(self.board_height)

    def validate_coords(self, from_coords, to_coords):
        """Check for errors in passed board coordinates.
        Args:
                from_coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
                to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
        Raises:
                IllegalMoveError
        """
        for coords in (from_coords, to_coords):
            if not self.coords_on_board(coords.x, coords.y):
                raise IllegalMoveError('Coordinates are not within board boundary')

        if from_coords == to_coords:
            raise IllegalMoveError('Move to same square illegal')

        if not self.board[from_coords.x][from_coords.y]:
            raise IllegalMoveError('No piece found at from coordinates')

    def coords_between(self, from_coords, to_coords):
        """Helper function. Return generator of all coords between from_coords and to_coords."""
        x_coords = self._coords_between(from_coords.x, to_coords.x, abs(from_coords.y - to_coords.y))
        y_coords = self._coords_between(from_coords.y, to_coords.y, abs(from_coords.x - to_coords.x))
        return (Coords(x, y) for x, y in zip(x_coords, y_coords))

    @staticmethod
    def _coords_between(from_coord, to_coord, other_coord_length):
        if from_coord > to_coord:
            return reversed(list(range(to_coord + 1, from_coord)))
        if from_coord == to_coord:
            return [from_coord] * other_coord_length
        return list(range(from_coord + 1, to_coord))

    def display_board(self):
        """Return board in correct position for display purposes"""
        transposed_board = [list(row) for row in zip(*self.board)]
        return list(reversed(transposed_board))

    def display_board_to_terminal(self):
        """Tabulate and display game board current state"""
        board = self.display_board()
        board.append(self.x_axis)
        print(tabulate(board, tablefmt="fancy_grid", showindex=self.y_axis))

    def process_coords(self, input_from_coords, input_to_coords):
        from_coords = self._coords_from(input_from_coords)
        to_coords = self._coords_from(input_to_coords)
        self.move(from_coords, to_coords)

    @staticmethod
    def _coords_from(input_coords):
        input_x, input_y = input_coords
        x_coords = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        y_coords = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
        x_coord, y_coord = x_coords[input_x], y_coords[input_y]
        return Coords(x_coord, y_coord)


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
    if from_coords.x != to_coords.x and from_coords.y == to_coords.y:
        return Direction.HORIZONTAL
    if from_coords.y != to_coords.y and from_coords.x == to_coords.x:
        return Direction.VERTICAL
    return Direction.NON_LINEAR


def adjacent_squares(from_coords, to_coords):
    """Check if to_coordinates are adjacent to from_coordinates. Return bool."""
    x_abs = abs(from_coords.x - to_coords.x)
    y_abs = abs(from_coords.y - to_coords.y)
    if x_abs == 0 or y_abs == 0:
        return x_abs + y_abs == 1
    return x_abs + y_abs == 2
