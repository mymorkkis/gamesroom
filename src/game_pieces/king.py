"""Module for King class."""
from src.game_enums import Color
from src.game_helper import adjacent_square, Coords
from src.game_pieces.game_piece import GamePiece


class King(GamePiece):
    """King chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.moved = False
        self.in_check = False

    def valid_move(self, to_coords):
        if not self.moved:
            return self._valid(to_coords) or self._valid_castle(to_coords)
        return self._valid(to_coords)

    def valid_capture(self, to_coords):
        return self._valid(to_coords)

    def _valid(self, to_coords):
        # King can only move/capture to an adjacent square (unless it's castling)
        return adjacent_square(self.coords, to_coords)

    def _valid_castle(self, to_coords):
        return (self.color == Color.WHITE and to_coords in (Coords(x=2, y=0), Coords(x=6, y=0))
                or self.color == Color.BLACK and to_coords in (Coords(x=2, y=7), Coords(x=6, y=7)))
