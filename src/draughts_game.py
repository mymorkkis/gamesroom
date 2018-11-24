from itertools import cycle

from src.game_enums import Color
from src.game import Coords, Game
from src.game_pieces.draughts_counter import Counter
from src.game_errors import IllegalMoveError


class DraughtsGame(Game):
    def __init__(self, restore_positions=None):
        super().__init__(
            board=[[None] * 8 for _ in range(8)],
            legal_piece_colors={Color.WHITE, Color.BLACK},
            legal_piece_names={'Counter'},
            restore_positions=restore_positions
        )
        self.playing_color = Color.BLACK
        self.opponent_color = Color.WHITE

    def move(self, from_coords, to_coords):
        self.set_move_attributes(from_coords, to_coords, self.playing_color)
        if self.playing_piece.legal_move(to_coords):
            self._move_piece()
        elif self.playing_piece.legal_capture(to_coords):
            self._capture_pieces()
            self._move_piece()
        else:
            raise IllegalMoveError('Illegal move attempted')
        self._switch_players()

    def _switch_players(self):
        playing_color = self.playing_color
        self.playing_color = self.opponent_color
        self.opponent_color = playing_color

    def _move_piece(self):
        self.board[self.from_coords.x][self.from_coords.y] = None
        self.board[self.to_coords.x][self.to_coords.y] = self.playing_piece
        self.playing_piece.coords = self.to_coords

    def _capture_pieces(self):
        if self._two_move_multiple_direction_capture():
            self._two_move_capture()
        elif self._three_move_multiple_direction_capture():
            self._three_move_capture()
        else:  # one direction capture
            self._capture(self.from_coords, self.to_coords)

    def _y_coord_and_x_coords(self):
        y_coord = self.from_coords.y + 2
        x_coords = cycle([self.from_coords.x + 2, self.from_coords.x - 2])
        if self.playing_color == Color.BLACK:
            y_coord = self.from_coords.y - 2
            next(x_coords)
        return y_coord, x_coords

    def _two_move_capture(self):
        y_coord, x_coords = self._y_coord_and_x_coords()
        second_capture_from = Coords(next(x_coords), y_coord)
        if self._capture_east_west_possible(second_capture_from):
            self._multi_direction_capture(second_capture_from)
        else:
            second_capture_from = Coords(next(x_coords), y_coord)
            if self._capture_west_east_possible(second_capture_from):
                self._multi_direction_capture(second_capture_from)

    def _three_move_capture(self):
        y_coord, x_coords = self._y_coord_and_x_coords()
        second_capture_from = Coords(next(x_coords), y_coord)
        if self._capture_east_west_possible(second_capture_from):
            third_capture_from = self._third_capture_from_coords(second_capture_from)
            if self._third_capture_possible(second_capture_from, third_capture_from):
                return
        second_capture_from = Coords(next(x_coords), y_coord)
        if self._capture_west_east_possible(second_capture_from):
            third_capture_from = self._third_capture_from_coords(second_capture_from)
            if self._third_capture_possible(second_capture_from, third_capture_from):
                return
        second_capture_from = Coords(next(x_coords), y_coord)
        if self._capture_east_east_possible(second_capture_from):
            third_capture_from = self._third_capture_from_coords(second_capture_from, change_x_coord=True)
            if self._third_capture_possible(second_capture_from, third_capture_from):
                return
        second_capture_from = Coords(next(x_coords), y_coord)
        if self._capture_west_west_possible(second_capture_from):
            third_capture_from = self._third_capture_from_coords(second_capture_from, direction='west_west')
            if self._third_capture_possible(second_capture_from, third_capture_from):
                return

    def _third_capture_from_coords(self, second_capture_from, direction=None, change_x_coord=False):
        # TODO Needs improving
        if self.playing_color == Color.WHITE:
            if change_x_coord:
                x_coord = second_capture_from.x + 2
            elif direction == 'west_west':
                x_coord = second_capture_from.x - 2
            else:
                x_coord = self.from_coords.x
            return Coords(x_coord, second_capture_from.y + 2)
        if change_x_coord:
            x_coord = second_capture_from.x - 2
        elif direction == 'west_west':
            x_coord = second_capture_from.x + 2
        else:
            x_coord = self.from_coords.x
        return Coords(x_coord, second_capture_from.y - 2)


    def _third_capture_possible(self, second_capture_from, third_capture_from):
        if self._capture_east_possible(third_capture_from):
            self._multi_direction_capture(second_capture_from, third_capture_from)
            return True
        if self._capture_west_possible(third_capture_from):
            self._multi_direction_capture(second_capture_from, third_capture_from)
            return True
        return False

    def _capture_east_west_possible(self, second_capture_from):
        return (self._capture_east_possible(self.from_coords)
                and self._capture_west_possible(second_capture_from))

    def _capture_west_west_possible(self, second_capture_from):
        return (self._capture_west_possible(self.from_coords)
                and self._capture_west_possible(second_capture_from))

    def _capture_west_east_possible(self, second_capture_from):
        return (self._capture_west_possible(self.from_coords)
                and self._capture_east_possible(second_capture_from))

    def _capture_east_east_possible(self, second_capture_from):
        return (self._capture_east_possible(self.from_coords)
                and self._capture_east_possible(second_capture_from))

    def _capture_east_possible(self, from_coords):
        try:
            if self.playing_color == Color.WHITE:
                return (self.board[from_coords.x + 1][from_coords.y + 1] == Counter(self.opponent_color)
                        and self.board[from_coords.x + 2][from_coords.y + 2] is None)
            return (self.board[from_coords.x - 1][from_coords.y - 1] == Counter(self.opponent_color)
                    and self.board[from_coords.x - 2][from_coords.y - 2] is None)
        except IndexError:
            return False

    def _capture_west_possible(self, from_coords):
        try:
            if self.playing_color == Color.WHITE:
                return (self.board[from_coords.x - 1][from_coords.y + 1] == Counter(self.opponent_color)
                        and self.board[from_coords.x - 2][from_coords.y + 2] is None)
            return (self.board[from_coords.x + 1][from_coords.y - 1] == Counter(self.opponent_color)
                    and self.board[from_coords.x + 2][from_coords.y - 2] is None)
        except IndexError:
            return False

    def _two_move_multiple_direction_capture(self):
        if self.playing_piece.color == Color.WHITE:
            return (self.to_coords.y == self.from_coords.y + 4
                    and self.to_coords.x == self.from_coords.x)
        return (self.to_coords.y == self.from_coords.y - 4
                and self.to_coords.x == self.from_coords.x)

    def _three_move_multiple_direction_capture(self):
        legal_x_coords = (self.from_coords.x - 2, self.from_coords.x + 2)
        if self.playing_piece.color == Color.WHITE:
            return (self.to_coords.y == self.from_coords.y + 6
                    and self.to_coords.x in legal_x_coords)
        return (self.to_coords.y == self.from_coords.y - 6
                and self.to_coords.x in legal_x_coords)

    def _multi_direction_capture(self, second_capture_from, third_capture_from=None):
        if third_capture_from:
            self._capture(self.from_coords, second_capture_from)
            self._capture(second_capture_from, third_capture_from)
            self._capture(third_capture_from, self.to_coords)
        else:
            self._capture(self.from_coords, second_capture_from)
            self._capture(second_capture_from, self.to_coords)

    def _capture(self, from_coords, to_coords):
        captured_pieces = []
        for idx, captured_piece_coords in enumerate(self.coords_between(from_coords, to_coords)):
            if idx % 2 == 0:
                captured_piece = self.board[captured_piece_coords.x][captured_piece_coords.y]
                if not captured_piece:
                    raise IllegalMoveError('Illegal capture attempted. No piece to capture')
                captured_pieces.append(captured_piece)
            else:
                if self.board[captured_piece_coords.x][captured_piece_coords.y] is not None:
                    raise IllegalMoveError('Illegal capture attempted. Piece blocking move')
        for captured_piece in captured_pieces:
            self.board[captured_piece.coords.x][captured_piece.coords.y] = None

    @staticmethod
    def new_setup():
        return draught_start_pieces()


def draught_start_pieces():
    """Return dictionary of new draughts game default piece postitions.

    Dictionary is in following format:
    key = str representation of game coordinates xy
    value = draughts GamePiece
    e.g '00': Counter(Color.WHITE)
    """
    x_axis_nums = cycle([0, 2, 4, 6, 1, 3, 5, 7])
    y_axis_nums = [0, 1, 2, 5, 6, 7]
    pieces = {}

    for y_axis_num in y_axis_nums:
        color = Color.WHITE if y_axis_num < 3 else Color.BLACK
        for _ in range(4):
            coords = f'{next(x_axis_nums)}{y_axis_num}'
            pieces[coords] = Counter(color)

    return pieces