from itertools import cycle, product

from src.game_enums import Color
from src.game import Game, NEXT_ADJACENT_COORD
from src.game_pieces.draughts_counter import Counter
from src.game_errors import IllegalMoveError


class DraughtsGame(Game):
    MAX_CAPTURE_MOVE_COUNT = 4

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
        self.validate_coords(from_coords, to_coords)
        self.set_move_attributes(from_coords, to_coords, self.playing_color)

        if self.playing_piece.legal_move(to_coords) and not self._potential_capture():
            self._move_piece()
        elif self.playing_piece.legal_capture(to_coords):
            capture_coords = self._collect_capture_coords()
            self._capture_pieces(capture_coords)
            self._force_capture_if_extra_captures_possible()
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
            self._capture(self.coords_between(*coords))

    def _capture(self, capture_coords):
        captured_piece_coords = (coords for idx, coords in enumerate(capture_coords) if idx % 2 == 0)
        for coords in captured_piece_coords:
            self.board[coords.x][coords.y] = None

    def _capture_move_count(self):
        if self.playing_piece.crowned:
            return self.MAX_CAPTURE_MOVE_COUNT
        return int(abs(self.from_coords.y - self.to_coords.y) / 2)

    def _collect_capture_coords(self):
        capture_coords = []
        direction_combinations = product(self.playing_piece.legal_move_directions(), repeat=self._capture_move_count())
        for combination in direction_combinations:
            coords = self.from_coords
            for direction in combination:
                if not coords:
                    break
                coords = self._capture_coords(direction, coords)
                capture_coords.append(coords)
                if self._move_route_found(capture_coords):
                    return (self.from_coords, *capture_coords)
            capture_coords = []
        raise IllegalMoveError('Illegal capture attempted. No piece to capture or piece blocking move')

    def _move_route_found(self, capture_coords):
        return capture_coords[-1] == self.to_coords

    def _king_row_reached(self):
        if self.playing_color == Color.WHITE:
            return self.playing_piece.coords.y == 7
        return self.playing_piece.coords.y == 0

    def _potential_capture(self):
        for piece in self._playing_pieces():
            for direction in piece.legal_move_directions():
                if self._capture_coords(direction, piece.coords):
                    raise IllegalMoveError('Move Illegal as capture is possible')
        return False

    def _playing_pieces(self):
        return (piece for row in self.board
                for piece in row if piece
                and piece.color == self.playing_color)

    def _force_capture_if_extra_captures_possible(self):
        from_coords = self.to_coords
        while from_coords:
            for direction in self.playing_piece.legal_move_directions():
                to_coords = self._capture_coords(direction, from_coords)
                if to_coords:
                    self._capture(self.coords_between(from_coords, to_coords))
                    self.to_coords = to_coords
                    # TODO message to screen?
            from_coords = to_coords if to_coords else None

    def _capture_coords(self, direction, from_coords):
        capture_coords = NEXT_ADJACENT_COORD[direction](from_coords)
        to_coords = NEXT_ADJACENT_COORD[direction](capture_coords)

        for coords in (capture_coords, to_coords):
            if not self.coords_on_board(coords):
                return None

        capture_square = self.board[capture_coords.x][capture_coords.y]
        move_to_square = self.board[to_coords.x][to_coords.y]

        if capture_square == Counter(self.opponent_color) and move_to_square is None:
            return to_coords
        return None

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
