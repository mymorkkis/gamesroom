"""Contains Othello game class."""
from src.game_enums import Color
from src.game_pieces.othello_disc import Disc
from src.game_errors import IllegalMoveError
from src.game import Coords, Game, NEXT_ADJACENT_COORD, ONE_COORD_ERR_MSG


class OthelloGame(Game):
    """Game logic for Othello."""

    ILLEGAL_MOVE = 'Either incorrect coords or move not trapping opponent discs'

    def __init__(self, restore_positions=None):

        OTHELLO_SETUP = {
            'board': [[None] * 8 for _ in range(8)],
            'legal_piece_colors': {Color.WHITE, Color.BLACK},
            'legal_piece_names': {'Disc'},
            'start_color': Color.BLACK,
            'input_err_msg': ONE_COORD_ERR_MSG
        }

        super().__init__(OTHELLO_SETUP, restore_positions)

    def make_move(self):
        for disc in self._trapped_discs(self.to_coords):
            disc.color = self.playing_color

        self._place_disc(self.to_coords)
        self._declare_winner_or_switch_players()

    def _declare_winner_or_switch_players(self):
        if not self._empty_square_coords():
            self.winner = self._winning_color()
        elif self._next_player_cant_move():
            self.switch_players()
            if self._next_player_cant_move():
                self.winner = self._winning_color()
        else:
            self.switch_players()

    def _winning_color(self):
        white_discs = self.disc_count(Color.WHITE)
        black_discs = self.disc_count(Color.BLACK)

        if white_discs > black_discs:
            return Color.WHITE
        if white_discs < black_discs:
            return Color.BLACK
        return Color.NONE

    def _place_disc(self, to_coords):
        disc = Disc(self.playing_color)
        self.board[to_coords.x][to_coords.y] = disc
        disc.coords = to_coords

    def _trapped_discs(self, to_coords):
        trapped_discs = self._scan_board_for_trapped_discs(to_coords)

        if not trapped_discs:
            raise IllegalMoveError(self.ILLEGAL_MOVE)

        return trapped_discs

    def _next_player_cant_move(self):
        empty_square_coords = self._empty_square_coords()

        for square_coords in empty_square_coords:
            trapped_discs = self._scan_board_for_trapped_discs(passed_coords=square_coords,
                                                               scan_all_directions=False)
            if trapped_discs:
                return False
        return True

    def _scan_board_for_trapped_discs(self, passed_coords, scan_all_directions=True):
        trapped_discs = []
        for direction in 'N NE E SE S SW W NW'.split():
            next_coords = passed_coords
            possible_trapped_discs = []
            while True:
                next_coords = NEXT_ADJACENT_COORD[direction](next_coords)
                if not self.coords_on_board(next_coords):
                    break
                disc = self.board[next_coords.x][next_coords.y]
                if not disc:
                    break
                elif disc.color == self.opponent_color:
                    possible_trapped_discs.append(disc)
                else:
                    trapped_discs.extend(possible_trapped_discs)
                    if trapped_discs and not scan_all_directions:
                        return trapped_discs
                    break
        return trapped_discs

    def _empty_square_coords(self):
        empty_square_coords = []
        for x_idx, row in enumerate(self.board):
            for y_idx, disc in enumerate(row):
                if not disc:
                    empty_square_coords.append(Coords(x_idx, y_idx))
        return empty_square_coords

    def disc_count(self, color):
        """Return int count of discs for given Disc color."""
        return len([disc for row in self.board
                    for disc in row
                    if disc and disc.color == color])

    @staticmethod
    def _new_board_setup():
        return {
            '34': Disc(Color.WHITE),
            '43': Disc(Color.WHITE),
            '33': Disc(Color.BLACK),
            '44': Disc(Color.BLACK),
        }
