"""Module for Knight class."""
from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece


class Knight(GamePiece):
    """Knight chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def __str__(self):
        return '\u2658' if self.color == Color.WHITE else '\u265E'

    def legal_move(self, to_coords):
        return self._legal(to_coords)

    def legal_capture(self, to_coords):
        return self._legal(to_coords)

    def _legal(self, to_coords):
        from_x, from_y = self.coords.x, self.coords.y
        to_x, to_y = to_coords.x, to_coords.y
        # Only the following 8 combinations of move/capture legal
        if (to_x == from_x + 1 and to_y in (from_y + 2, from_y - 2)
                or to_x == from_x + 2 and to_y in (from_y + 1, from_y - 1)
                or to_x == from_x - 1 and to_y in (from_y + 2, from_y - 2)
                or to_x == from_x - 2 and to_y in (from_y + 1, from_y - 1)):
            return True
        return False
