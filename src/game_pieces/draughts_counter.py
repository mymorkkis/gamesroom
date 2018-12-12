from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece
from src.games.game import NEXT_ADJACENT_COORD

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

    def legal_move_directions(self):
        if self.crowned:
            return ['NE', 'SE', 'SW', 'NW']
        return ['NE', 'NW'] if self.color == Color.WHITE else ['SE', 'SW']

    def legal_move(self, to_coords):
        for direction in self.legal_move_directions():
            if to_coords == NEXT_ADJACENT_COORD[direction](self.coords):
                return True
        return False

    def legal_capture(self, to_coords):
        # Only cursory check here. Main capture logic in Draughts game
        for coords in (self.coords, to_coords):
            if self._white_square(coords):
                return False
        return True

    def _white_square(self, coords):
        return (coords.x + coords.y) % 2 != 0
