from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece

class Counter(GamePiece):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.crowned = False

    def __str__(self):
        if self.crowned:
            return '\u26C1' if self.color == Color.WHITE else '\u26C3'
        return '\u26C0' if self.color == Color.WHITE else '\u26C2'

    def legal_move(self, to_coords):
        legal_x_coords = (self.coords.x + 1, self.coords.x - 1)
        legal_y_coord = self.coords.y + 1 if self.color == Color.WHITE else self.coords.y - 1
        return to_coords.x in legal_x_coords and to_coords.y == legal_y_coord

    def legal_capture(self, to_coords):
        legal_x_coords = (self.coords.x + 2, self.coords.x - 2)
        legal_y_coord = self.coords.y + 2 if self.color == Color.WHITE else self.coords.y - 2
        return to_coords.x in legal_x_coords and to_coords.y == legal_y_coord
