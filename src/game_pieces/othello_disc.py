"""Contains Disc object for use in games such as Othello."""
from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece

class Disc(GamePiece):
    """Disc is a dumb object. Can only be placed or flipped so doesn't implement legal move/capture."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def __str__(self):
        return '\u25EF' if self.color == Color.WHITE else '\u2B24'

    def legal_move(self, to_coords):
        raise NotImplementedError()

    def legal_capture(self, to_coords):
        raise NotImplementedError()
