"""Module for Pawn class."""
from src.game_pieces.game_piece import GamePiece


class Pawn(GamePiece):
    """Pawn chess game piece. Inherits from GamePiece."""
    def __init__(self, *, color):
        super().__init__()
        self.color = color

    def valid_move(self, coords):
        # TODO Add first move functionality for two spaces
        if coords.x == self.x_coord and coords.y == self._valid_y_coord():
            return True
        return False

    def valid_capture(self, coords):
        if ((coords.x == self.x_coord + 1 or coords.x == self.x_coord - 1)
                and coords.y == self._valid_y_coord()):
            return True
        return False

    def _valid_y_coord(self):
        if self.color == 'white':
            valid_y_coord = self.y_coord + 1
        elif self.color == 'black':
            valid_y_coord = self.y_coord - 1
        return valid_y_coord
