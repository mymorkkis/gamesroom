"""Module for King class."""
from src.game_pieces.game_piece import GamePiece


class King(GamePiece):
    """King chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def valid_move(self, to_coords):
        return self._valid(to_coords)

    def valid_capture(self, to_coords):
        return self._valid(to_coords)

    def _valid(self, to_coords):
        x_abs = abs(self.coords.x - to_coords.x)
        y_abs = abs(self.coords.y - to_coords.y)
        # King can only move/capture one space along
        if x_abs + y_abs in (1, 2):
            return True
        return False
