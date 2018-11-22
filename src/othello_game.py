from src.game_enums import Color
from src.game_pieces.othello_disc import Disc
from src.game import Game

class Othello(Game):
    def __init__(self, restore_positions=None):
        super().__init__(
            board=[[None] * 8 for _ in range(8)],
            legal_piece_colors={Color.WHITE, Color.BLACK},
            legal_piece_names={'Disc'},
            restore_positions=restore_positions
        )

    @staticmethod
    def new_setup():
        return {
            '34': Disc(Color.WHITE),
            '43': Disc(Color.WHITE),
            '33': Disc(Color.BLACK),
            '44': Disc(Color.BLACK),
        }

    def move(self, from_coords, to_coords):
        pass
