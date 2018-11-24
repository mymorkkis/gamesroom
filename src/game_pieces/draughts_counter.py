from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece

class Counter(GamePiece):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.crowned = False
        self._to_coords = None

    def __str__(self):
        if self.crowned:
            return '\u26C1' if self.color == Color.WHITE else '\u26C3'
        return '\u26C0' if self.color == Color.WHITE else '\u26C2'

    def legal_move(self, to_coords):
        legal_x_coords = (self.coords.x + 1, self.coords.x - 1)
        legal_y_coord = self.coords.y + 1 if self.color == Color.WHITE else self.coords.y - 1
        return to_coords.x in legal_x_coords and to_coords.y == legal_y_coord

    def legal_capture(self, to_coords):
        self._to_coords = to_coords
        legal_x_coords, legal_y_coord = None, None

        if self.color == Color.WHITE:
            if self._white_one_piece_capture():
                legal_x_coords = (self.coords.x + 2, self.coords.x - 2)
                legal_y_coord = self.coords.y + 2
            elif self._white_two_piece_capture():
                legal_x_coords = (self.coords.x + 4, self.coords.x, self.coords.x - 4)
                legal_y_coord = self.coords.y + 4
            elif self._white_three_piece_capture():
                legal_x_coords = (self.coords.x + 2, self.coords.x - 2)
                legal_y_coord = self.coords.y + 6
        else:
            if self._black_one_piece_capture():
                legal_x_coords = (self.coords.x + 2, self.coords.x - 2)
                legal_y_coord = self.coords.y - 2
            elif self._black_two_piece_capture():
                legal_x_coords = (self.coords.x + 4, self.coords.x, self.coords.x - 4)
                legal_y_coord = self.coords.y - 4
            elif self._black_three_piece_capture():
                legal_x_coords = (self.coords.x + 2, self.coords.x - 2)
                legal_y_coord = self.coords.y - 6

        if legal_x_coords and 0 <= legal_y_coord <= 7:
            return to_coords.x in legal_x_coords and to_coords.y == legal_y_coord
        return False

    def _white_one_piece_capture(self):
        return self._to_coords.y == self.coords.y + 2

    def _white_two_piece_capture(self):
        return self._to_coords.y == self.coords.y + 4

    def _white_three_piece_capture(self):
        return self._to_coords.y == self.coords.y + 6

    def _black_one_piece_capture(self):
        return self._to_coords.y == self.coords.y - 2

    def _black_two_piece_capture(self):
        return self._to_coords.y == self.coords.y - 4

    def _black_three_piece_capture(self):
        return self._to_coords.y == self.coords.y - 6