from itertools import cycle

from src.game_enums import Color
from src.game import Game
from src.game_pieces.draughts_counter import Counter


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

    def move(self):
        pass

    @staticmethod
    def new_setup():
        return draught_start_pieces()


def draught_start_pieces():
    x_axis_nums = cycle([0, 2, 4, 6, 1, 3, 5, 7])
    y_axis_nums = [0, 1, 2, 5, 6, 7]
    pieces = {}

    for y_axis_num in y_axis_nums:
        color = Color.WHITE if y_axis_num < 3 else Color.BLACK
        for _ in range(4):
            coords = f'{y_axis_num}{next(x_axis_nums)}'
            pieces[coords] = Counter(color)

    return pieces