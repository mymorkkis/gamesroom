"""Module for Pawn class."""
from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece


class Pawn(GamePiece):
    """Pawn chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def valid_move(self, coords):
        # TODO Add first move functionality for two spaces
        if coords.x == self.x_coord and self._valid_y_coord(coords.y):
            return True
        return False

    def valid_capture(self, coords):
        if ((coords.x == self.x_coord + 1 or coords.x == self.x_coord - 1)
                and self._valid_y_coord(coords.y, capture=True)):
            return True
        return False

    def _valid_y_coord(self, move_y_coord, capture=False):
        valid = False
        if self.color == Color.WHITE:
            if move_y_coord == self.y_coord + 1:
                valid = True
            if not capture and self.y_coord == 1 and move_y_coord == self.y_coord + 2:
                # Two spaces forward allowed on Pawn first move
                valid = True
        elif self.color == Color.BLACK:
            if move_y_coord == self.y_coord - 1:
                valid = True
            if not capture and self.y_coord == 6 and move_y_coord == self.y_coord - 2:
                # Two spaces forward allowed on Pawn first move
                valid = True
        return valid
