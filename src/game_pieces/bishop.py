"""Module for Bishop class."""
from src.game_enums import Direction
from src.game_pieces.game_piece import GamePiece
from src.game_helper import Coords, move_direction


class Bishop(GamePiece):
    """Bishop chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def valid_move(self, to_coords):
        return self._valid(to_coords)

    def valid_capture(self, to_coords):
        return self._valid(to_coords)

    def _valid(self, to_coords):
        from_coords = Coords(x=self.x_coord, y=self.y_coord)
        # Any diagonal move/capture valid for Bishop
        if move_direction(from_coords, to_coords) == Direction.DIAGONAL:
            return True
        return False
