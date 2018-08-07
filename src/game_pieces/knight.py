"""Module for Knight class."""
from src.game_pieces.game_piece import GamePiece


class Knight(GamePiece):
    """Knight chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def valid_move(self, to_coords):
        return self._valid(to_coords)

    def valid_capture(self, to_coords):
        return self._valid(to_coords)

    def _valid(self, to_coords):
        from_x, from_y = self.coords.x, self.coords.y
        to_x, to_y = to_coords.x, to_coords.y
        # Only the following 8 combinations of move/capture valid
        if (to_x == from_x + 1 and to_y in (from_y + 2, from_y - 2)
                or to_x == from_x + 2 and to_y in (from_y + 1, from_y - 1)
                or to_x == from_x - 1 and to_y in (from_y + 2, from_y - 2)
                or to_x == from_x - 2 and to_y in (from_y + 1, from_y - 1)):
            return True
        return False
