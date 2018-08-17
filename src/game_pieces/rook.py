"""Module for Rook class."""
from src.game_enums import Direction
from src.game_pieces.game_piece import GamePiece
from src.game_helper import move_direction


class Rook(GamePiece):
    """Rook chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def valid_move(self, to_coords):
        return self._valid(to_coords)

    def valid_capture(self, to_coords):
        return self._valid(to_coords)

    def _valid(self, to_coords):
        # Any vertical or horizontal move/capture valid for Rook
        if move_direction(self.coords, to_coords) in (Direction.VERTICAL, Direction.HORIZONTAL):
            return True
        return False
