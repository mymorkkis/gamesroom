"""Module for Queen class."""
from src.game_pieces.game_piece import GamePiece
from src.game_helper import move_direction


class Queen(GamePiece):
    """Queen chess game piece. Inherits from GamePiece."""
    def __init__(self, *, color):
        super().__init__()
        self.color = color

    def valid_move(self, coords):
        return self._valid(coords)

    def valid_capture(self, coords):
        return self._valid(coords)

    def _valid(self, coords):
        # Any linear move/capture valid for Queen
        if move_direction(self, coords) != 'non_linear':
            return True
        return False
