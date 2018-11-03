"""Module for King class."""
from src.game_enums import Color
from src.game import adjacent_squares, Coords
from src.game_pieces.game_piece import GamePiece


class King(GamePiece):
    """King chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.moved = False

    def __str__(self):
        # Colors inverted as I use dark terminal
        return '\U0000265A' if self.color == Color.WHITE else '\U00002654'

    def legal_move(self, to_coords):
        if not self.moved:
            return self._legal(to_coords) or self._legal_castle(to_coords)
        return self._legal(to_coords)

    def legal_capture(self, to_coords):
        return self._legal(to_coords)

    def _legal(self, to_coords):
        return adjacent_squares(self.coords, to_coords)

    def _legal_castle(self, to_coords):
        return (self.color == Color.WHITE and to_coords in (Coords(x=2, y=0), Coords(x=6, y=0))
                or self.color == Color.BLACK and to_coords in (Coords(x=2, y=7), Coords(x=6, y=7)))
