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
        return '\u2654' if self.color == Color.WHITE else '\u265A'

    def legal_move(self, to_coords):
        if not self.moved:
            return self._legal(to_coords) or self._legal_castle(to_coords)
        return self._legal(to_coords)

    def legal_capture(self, to_coords):
        return self._legal(to_coords)

    def _legal(self, to_coords):
        return adjacent_squares(self.coords, to_coords)

    def _legal_castle(self, to_coords):
        return (self.color == Color.WHITE and to_coords in (Coords(x='c', y='1'), Coords(x='g', y='1'))
                or self.color == Color.BLACK and to_coords in (Coords(x='c', y='8'), Coords(x='g', y='8')))
