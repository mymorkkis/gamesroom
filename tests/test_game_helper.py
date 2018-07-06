"""Test module form game_helper module."""
from collections import namedtuple
import unittest

from src.chess_game import ChessGame
from src.game_enums import Color, Direction
from src.game_helper import move_direction
from src.game_pieces.pawn import Pawn


class GameHelperTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.pawn = Pawn(Color.BLACK)
        self.chess_game = ChessGame()
        self.coords = namedtuple('Coords', 'x y')
        self.start_coords = self.coords(x=4, y=4)
        self.chess_game.add(self.pawn, self.start_coords)

    def test_move_direction_diagonal_up(self):
        to_coords = self.coords(x=2, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.DIAGONAL

    def test_move_direction_diagonal_down(self):
        to_coords = self.coords(x=6, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.DIAGONAL

    def test_move_direction_horizontal(self):
        to_coords = self.coords(x=2, y=4)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.HORIZONTAL

    def test_move_direction_horizontal(self):
        to_coords = self.coords(x=6, y=4)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.HORIZONTAL

    def test_move_direction_vertical(self):
        to_coords = self.coords(x=4, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.VERTICAL

    def test_move_direction_vertical(self):
        to_coords = self.coords(x=4, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.VERTICAL

    def test_move_direction_non_linear(self):
        to_coords = self.coords(x=5, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.NON_LINEAR

    def test_move_direction_non_linear(self):
        to_coords = self.coords(x=3, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == Direction.NON_LINEAR
