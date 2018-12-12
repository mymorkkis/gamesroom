"""Main game module with Game abstract base class.

   Functions:
        move_direction:   return move Direction enum type
        adjacent_squares: return bool
"""
from abc import ABC, abstractmethod
from collections import namedtuple
from pathlib import Path
import pickle

from tabulate import tabulate

from src.game_enums import Color, Direction
from src.game_errors import IllegalMoveError, NotOnBoardError


ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
ONE_COORD_ERR_MSG = 'Invalid coords. Example usage: a1'
TWO_COORD_ERR_MSG = 'Invalid coords, coords seperated by white space. Example usage: a1 a2'


Coords = namedtuple('Coords', 'x y')


class Game(ABC):
    """Abstract Base class for game.

       Methods:
            add
            move
            coords_on_board
            coords_between
            switch_players
            opponenet_color
            x_axis
            y_axis
            display_board
            display_board_to_terminal
            gui_display_board
            save_game

       Abstract methods:
            make_move
            _new_board_setup
    """
    SAME_SQUARE = 'Move to same square illegal'
    NO_PIECE = 'No piece found at from coordinates'
    WRONG_COLOR = 'Incorrect piece color for current player'
    SQUARE_TAKEN = 'Piece already found at coordinates'

    def __init__(self, setup, restore_positions):
        self.board = setup['board']
        self.board_width = len(self.board[0])
        self.board_height = len(self.board)
        self.legal_piece_names = setup['legal_piece_names']
        self.legal_piece_colors = setup['legal_piece_colors']
        self.input_error_msg = setup['input_err_msg']
        self._setup_game(restore_positions)
        # Move attributes
        self.playing_color = setup['start_color']
        self.move_error_msg = None
        self.from_coords = None
        self.to_coords = None
        self.playing_piece = None
        self.winner = None

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __str__(self):
        return tabulate(self.display_board(), tablefmt="fancy_grid")

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.board, self.playing_color) == (other.board, other.playing_color)
        return NotImplemented

    @abstractmethod
    def make_move(self):
        """Move piece from coordinates, to coordianates. Remove captured piece, if any.
           Args:
                from_coords: Namedtuple with coordinates x & y. E.g. Coords(x='a', y='2').
                to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x='a', y='2').
           Raises:
                IllegalMoveError
        """
        raise NotImplementedError()

    @abstractmethod
    def _new_board_setup(self):
        """Return dictionary of new game default piece start postitions and pieces.

        Dictionary is in following format:
        key = str representation of game coordinates xy
        value = GamePiece
        e.g '00': Piece(Color.WHITE)
        """
        raise NotImplementedError()

    def _setup_game(self, restore_positions):
        """Setup board for new or previously stored game."""
        game_positions = self._new_board_setup() if restore_positions is None else restore_positions

        for coords, piece in game_positions.items():
            assert piece.color in self.legal_piece_colors
            assert piece.name in self.legal_piece_names
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            self.add(piece, coords)

    def move(self, *input_coords):
        """Move piece from coordinates, to coordianates. Remove captured piece, if any.
           Args (optional):
                from_coords: Chess notation str, eg a1
           Args:
                to_coords:   Chess notation str, eg a2
           Raises:
                IllegalMoveError
        """
        processed_coords = []
        for coords in input_coords:
            try:
                processed_coords.append(self._coords_from(coords))
            except (ValueError, KeyError):
                raise IllegalMoveError(self.input_error_msg)
        self._set_current_move_attributes_or_raise_errors(*reversed(processed_coords))
        self.make_move()

    @staticmethod
    def _coords_from(input_coords):
        input_x, input_y = input_coords
        x_coords = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        y_coords = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
        x_coord, y_coord = x_coords[str(input_x).lower()], y_coords[str(input_y)]
        return Coords(x_coord, y_coord)

    @classmethod
    def restore(cls, file_name):
        """Restore previously saved game state from saved_games folder."""
        file_path = Path.cwd() / 'saved_games' / file_name

        try:
            with open(file_path, 'rb') as from_file:
                restored_game = pickle.load(from_file)
                return restored_game
        except FileNotFoundError:
            # TODO Handle this with gui error msg
            return None

    def save(self, file_name):
        """Save current game state to pickle file in saved_games folder."""
        file_path = Path.cwd() / 'saved_games' / file_name

        with open(file_path, 'wb') as to_file:
            pickle.dump(self, to_file)

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

    def switch_players(self):
        """For games with two game colors. Switch player and opponent colors."""
        self.playing_color = self.opponent_color

    @property
    def opponent_color(self):
        """Return Color enum type of opponent color to current playing color."""
        return Color.WHITE if self.playing_color == Color.BLACK else Color.BLACK

    def _move_piece_and_update_coords(self):
        self.board[self.from_coords.x][self.from_coords.y] = None
        self.board[self.to_coords.x][self.to_coords.y] = self.playing_piece
        self.playing_piece.coords = self.to_coords

    def current_board_pieces(self):
        """Generator of all pieces currently on game board."""
        for row in self.board:
            for piece in row:
                if piece:
                    yield piece

    def coords_on_board(self, coords):
        """Check if coordinates within board range (negative indexing not allowed). Return bool."""
        return coords.x in range(self.board_width) and coords.y in range(self.board_height)

    def _set_current_move_attributes_or_raise_errors(self, to_coords=None, from_coords=None):
        if from_coords:
            if from_coords == to_coords:
                raise IllegalMoveError(self.SAME_SQUARE)

            if not self.board[from_coords.x][from_coords.y]:
                raise IllegalMoveError(self.NO_PIECE)

            self.from_coords = from_coords
            self.to_coords = to_coords
            self.playing_piece = self.board[from_coords.x][from_coords.y]

            if self.playing_piece.color != self.playing_color:
                raise IllegalMoveError(self.WRONG_COLOR)
        else:
            if self.board[to_coords.x][to_coords.y]:
                raise IllegalMoveError(self.SQUARE_TAKEN)

            self.to_coords = to_coords


    def coords_between(self, from_coords, to_coords):
        """Return generator of all Coords(x, y) between from_coords and to_coords."""
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

    def x_axis(self):
        """Return list of letters in range a-z for length of board x-axis width"""
        return list(ALPHABET[:self.board_width])

    def y_axis(self):
        """Return reversed list of ints for length of board y-axis height"""
        return list(reversed(range(self.board_height + 1)))

    def display_board(self):
        """Return board in correct position for display purposes"""
        transposed_board = [list(row) for row in zip(*self.board)]
        return list(reversed(transposed_board))

    def gui_display_board(self):
        """TODO messy board setup, must be more pythonic way"""
        display_board = []
        board = [self.x_axis()] + self.display_board() + [self.x_axis()]

        y_axis = [''] + self.y_axis()
        y_axis.pop()
        y_axis = y_axis + ['']

        for axis_no, board_row in zip(y_axis, board):
            board_row.insert(0, axis_no)
            board_row.append(axis_no)
            display_board.append(board_row)

        return display_board

    def display_board_to_terminal(self):
        """Tabulate and display game board current state"""
        board = self.display_board()
        board.append(self.x_axis())
        print(tabulate(board, tablefmt="fancy_grid", showindex=self.y_axis()))


def move_direction(from_coords, to_coords):
    """Calculate direction from from_coordinates to coordinates. Return Direction enum.
    Args:
            from_coords: Namedtuple with coordinates x & y. E.g. Coords(x='a', y='2').
            to_coords:   Namedtuple with coordinates x & y. E.g. Coords(x='a', y='2').
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


NEXT_ADJACENT_COORD = {
    'N': lambda c: Coords(c.x, c.y + 1),
    'NE': lambda c: Coords(c.x + 1, c.y + 1),
    'E': lambda c: Coords(c.x + 1, c.y),
    'SE': lambda c: Coords(c.x + 1, c.y - 1),
    'S': lambda c: Coords(c.x, c.y - 1),
    'SW': lambda c: Coords(c.x - 1, c.y - 1),
    'W': lambda c: Coords(c.x - 1, c.y),
    'NW': lambda c: Coords(c.x - 1, c.y + 1)
}
