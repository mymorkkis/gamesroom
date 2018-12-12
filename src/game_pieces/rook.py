"""Module for Rook class."""
from src.game_enums import Color, Direction
from src.game_pieces.game_piece import GamePiece
from src.games.game import move_direction


class Rook(GamePiece):
    """Rook chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.moved = False

    def __str__(self):
        return '\u2656' if self.color == Color.WHITE else '\u265C'

    def legal_move(self, to_coords):
        return self._legal(to_coords)

    def legal_capture(self, to_coords):
        return self._legal(to_coords)

    def _legal(self, to_coords):
        return move_direction(self.coords, to_coords) in (Direction.VERTICAL, Direction.HORIZONTAL)
