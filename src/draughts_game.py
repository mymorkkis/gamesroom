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

        if self.playing_piece.legal_move(to_coords) and not self._potential_capture():
            self._move_piece()
        elif self.playing_piece.legal_capture(to_coords):
            capture_coords = self._calculate_capture_coords()
            self._capture_pieces(capture_coords)
            self._force_capture_if_extra_capture_possible()
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
        if self._king_row_reached():
            self.playing_piece.crowned = True

    def _capture_pieces(self, capture_coords):
        from_coords, to_coords = capture_coords[:-1], capture_coords[1:]
        for coords in zip(from_coords, to_coords):
            self._capture(*coords)

    def _calculate_capture_coords(self):
        if self._two_move_multiple_direction_capture():
            return self._two_move_capture_coords()
        if self._three_move_multiple_direction_capture():
            return self._three_move_capture_coords()
        return self.from_coords, self.to_coords

    def _king_row_reached(self):
        if self.playing_color == Color.WHITE:
            return self.playing_piece.coords.y == 7
        return self.playing_piece.coords.y == 0

    def _potential_capture(self):
        for piece in self._playing_pieces():
            if (self._capture_east_possible(piece.coords)
                    or self._capture_west_possible(piece.coords)):
                raise IllegalMoveError('Move Illegal as capture is possible')
        return False

    def _playing_pieces(self):
        return (piece for row in self.board
                for piece in row if piece
                and piece.color == self.playing_color)

    def _force_capture_if_extra_capture_possible(self):
        for capture_possible in (self._capture_east_possible, self._capture_west_possible):
            coords = capture_possible(self.to_coords)
            if coords:
                self._capture(self.to_coords, coords)
                self.to_coords = coords
                # TODO message to screen?

    def _two_move_capture_coords(self):
        for two_move_capture in (self._capture_east_west, self._capture_west_east):
            capture_coords = two_move_capture()
            if self._move_route_found(capture_coords):
                return capture_coords
        assert False, 'Reached unexpected path in _two_move_capture_coords'

    def _three_move_capture_coords(self):
        for three_move_capture in self._three_move_capture_directions():
            capture_coords = three_move_capture()
            if self._move_route_found(capture_coords):
                return capture_coords
        assert False, 'Reached unexpected path in _three_move_capture_coords'

    def _three_move_capture_directions(self):
        return (self._capture_east_west_east, self._capture_east_west_west,
                self._capture_west_east_east, self._capture_west_east_west,
                self._capture_east_east_west, self._capture_west_west_east)

    def _move_route_found(self, capture_coords):
        return capture_coords and capture_coords[-1] == self.to_coords

    def _capture_east_west(self):
        second_capture_from_coords = self._capture_east_possible(self.from_coords)
        to_coords = self._capture_west_possible(second_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, to_coords)

    def _capture_west_east(self):
        second_capture_from_coords = self._capture_west_possible(self.from_coords)
        to_coords = self._capture_east_possible(second_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, to_coords)

    def _capture_east_west_east(self):
        second_capture_from_coords = self._capture_east_possible(self.from_coords)
        third_capture_from_coords = self._capture_west_possible(second_capture_from_coords)
        to_coords = self._capture_east_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_east_west_west(self):
        second_capture_from_coords = self._capture_east_possible(self.from_coords)
        third_capture_from_coords = self._capture_west_possible(second_capture_from_coords)
        to_coords = self._capture_west_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_west_east_east(self):
        second_capture_from_coords = self._capture_west_possible(self.from_coords)
        third_capture_from_coords = self._capture_east_possible(second_capture_from_coords)
        to_coords = self._capture_east_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_west_east_west(self):
        second_capture_from_coords = self._capture_west_possible(self.from_coords)
        third_capture_from_coords = self._capture_east_possible(second_capture_from_coords)
        to_coords = self._capture_west_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_east_east_west(self):
        second_capture_from_coords = self._capture_east_possible(self.from_coords)
        third_capture_from_coords = self._capture_east_possible(second_capture_from_coords)
        to_coords = self._capture_west_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_west_west_east(self):
        second_capture_from_coords = self._capture_west_possible(self.from_coords)
        third_capture_from_coords = self._capture_west_possible(second_capture_from_coords)
        to_coords = self._capture_east_possible(third_capture_from_coords)
        return self._capture_coords_or_none(second_capture_from_coords, third_capture_from_coords, to_coords)

    def _capture_coords_or_none(self, *move_coords):
        for coords in move_coords:
            if not coords:
                return None
        return (self.from_coords, *move_coords)

    def _capture_east_possible(self, from_coords):
        if not from_coords:
            return None

        if self.playing_color == Color.WHITE:
            capture_coords = Coords(from_coords.x + 1, from_coords.y + 1)
            to_coords = Coords(from_coords.x + 2, from_coords.y + 2)
        else:
            capture_coords = Coords(from_coords.x + 1, from_coords.y - 1)
            to_coords = Coords(from_coords.x + 2, from_coords.y - 2)

        if self._capture_possible(capture_coords, to_coords):
            return to_coords
        return None

    def _capture_west_possible(self, from_coords):
        if not from_coords:
            return None

        if self.playing_color == Color.WHITE:
            capture_coords = Coords(from_coords.x - 1, from_coords.y + 1)
            to_coords = Coords(from_coords.x - 2, from_coords.y + 2)
        else:
            capture_coords = Coords(from_coords.x - 1, from_coords.y - 1)
            to_coords = Coords(from_coords.x - 2, from_coords.y - 2)

        if self._capture_possible(capture_coords, to_coords):
            return to_coords
        return None

    def _capture_possible(self, capture_coords, to_coords):
        for coords in (capture_coords, to_coords):
            if not self.coords_on_board(coords):
                return False

        capture_square = self.board[capture_coords.x][capture_coords.y]
        move_to_square = self.board[to_coords.x][to_coords.y]

        return capture_square == Counter(self.opponent_color) and move_to_square is None

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
