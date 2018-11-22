from itertools import cycle

from src.game_enums import Color
from src.game_pieces.othello_disc import Disc
from src.game_errors import IllegalMoveError
from src.game import Game, NEXT_ADJACENT_COORD


class Othello(Game):
    def __init__(self, restore_positions=None):
        super().__init__(
            board=[[None] * 8 for _ in range(8)],
            legal_piece_colors={Color.WHITE, Color.BLACK},
            legal_piece_names={'Disc'},
            restore_positions=restore_positions
        )
        self.playing_colors = cycle([Color.BLACK, Color.WHITE])
        self.playing_color = next(self.playing_colors)

    @staticmethod
    def new_setup():
        return {
            '34': Disc(Color.WHITE),
            '43': Disc(Color.WHITE),
            '33': Disc(Color.BLACK),
            '44': Disc(Color.BLACK),
        }

    def move(self, to_coords):
        trapped_discs = self._trapped_discs(to_coords)

        if not trapped_discs:
            raise IllegalMoveError('Move must trap opponent discs')

        for disc in trapped_discs:
            disc.color = self.playing_color

        self._place_disc(to_coords)
        self.playing_color = next(self.playing_colors)

    def _place_disc(self, to_coords):
        disc = Disc(self.playing_color)
        self.board[to_coords.x][to_coords.y] = disc
        disc.coords = to_coords

    def _trapped_discs(self, to_coords):
        trapped_discs = []
        for direction in 'N NE E SE S SW W NW'.split():
            next_coords = to_coords
            possible_trapped_discs = []
            while True:
                next_coords = NEXT_ADJACENT_COORD[direction](next_coords)
                if not self.coords_on_board(next_coords.x, next_coords.y):
                    break
                disc = self.board[next_coords.x][next_coords.y]
                if not disc:
                    break
                elif disc.color == self.playing_color:
                    trapped_discs.extend(possible_trapped_discs)
                    break
                else:
                    possible_trapped_discs.append(disc)
        return trapped_discs
