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
        crowned_legal_y_coords = (self.coords.y + 1, self.coords.y - 1)
        legal_y_coord = self.coords.y + 1 if self.color == Color.WHITE else self.coords.y - 1
        if self.crowned:
            return to_coords.x in legal_x_coords and to_coords.y in crowned_legal_y_coords
        return to_coords.x in legal_x_coords and to_coords.y == legal_y_coord

    def legal_capture(self, to_coords):
        self._to_coords = to_coords
        if self.crowned:
            return self._legal_white_capture() or self._legal_black_capture()
        if self.color == Color.WHITE:
            return self._legal_white_capture()
        return self._legal_black_capture()

    def _legal_capture(self, x_coords, y_coord):
        return self._to_coords.x in x_coords and self._to_coords.y == y_coord

    def _legal_white_capture(self):
        if self._white_one_piece_capture():
            x_coords = (self.coords.x + 2, self.coords.x - 2)
            y_coord = self.coords.y + 2
            return self._legal_capture(x_coords, y_coord)
        if self._white_two_piece_capture():
            x_coords = (self.coords.x + 4, self.coords.x, self.coords.x - 4)
            y_coord = self.coords.y + 4
            return self._legal_capture(x_coords, y_coord)
        if self._white_three_piece_capture():
            x_coords = (self.coords.x + 2, self.coords.x - 2)
            y_coord = self.coords.y + 6
            return self._legal_capture(x_coords, y_coord)
        return False

    def _legal_black_capture(self):
        if self._black_one_piece_capture():
            x_coords = (self.coords.x + 2, self.coords.x - 2)
            y_coord = self.coords.y - 2
            return self._legal_capture(x_coords, y_coord)
        if self._black_two_piece_capture():
            x_coords = (self.coords.x + 4, self.coords.x, self.coords.x - 4)
            y_coord = self.coords.y - 4
            return self._legal_capture(x_coords, y_coord)
        if self._black_three_piece_capture():
            x_coords = (self.coords.x + 2, self.coords.x - 2)
            y_coord = self.coords.y - 6
            return self._legal_capture(x_coords, y_coord)
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
