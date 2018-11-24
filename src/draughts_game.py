from itertools import cycle

from src.game_enums import Color
from src.game import Game
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
        self._playing_colors = cycle([Color.BLACK, Color.WHITE])
        self.playing_color = next(self._playing_colors)

    def move(self, from_coords, to_cooords):
        piece = self.board[from_coords.x][from_coords.y]
        if piece.legal_move(to_cooords):
            self._move(piece, from_coords, to_cooords)
        elif piece.legal_capture(to_cooords):
            for captured_piece_coords in self.coords_between(from_coords, to_cooords):
                self.board[captured_piece_coords.x][captured_piece_coords.y] = None
            self._move(piece, from_coords, to_cooords)
        else:
            raise IllegalMoveError('Illegal move attempted')

    def _move(self, piece, from_coords, to_coords):
        self.board[from_coords.x][from_coords.y] = None
        self.board[to_coords.x][to_coords.y] = piece
        piece.coords = to_coords

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