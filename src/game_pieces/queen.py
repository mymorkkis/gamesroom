"""Module for Queen class."""
from src.game_enums import Direction
from src.game_pieces.game_piece import GamePiece
from src.game import move_direction


class Queen(GamePiece):
    """Queen chess game piece. Inherits from GamePiece."""
    def __init__(self, color):
        super().__init__()
        self.color = color

    def legal_move(self, to_coords):
        return self._legal(to_coords)

    def legal_capture(self, to_coords):
        return self._legal(to_coords)

    def _legal(self, to_coords):
        return move_direction(self.coords, to_coords) != Direction.NON_LINEAR
