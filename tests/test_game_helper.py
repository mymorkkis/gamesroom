"""Test module form ChessBoard class."""
from collections import namedtuple
import unittest

from src.chess_game import ChessGame
from src.game_helper import move_direction
from src.game_pieces.pawn import Pawn


class ChessGameTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.pawn = Pawn(color='black')
        self.chess_game = ChessGame()
        self.coords = namedtuple('Coords', 'x y')
        self.start_coords = self.coords(x=4, y=4)
        self.chess_game.add(self.pawn, self.start_coords)

    def test_move_direction_diagonal_up(self):
        to_coords = self.coords(x=2, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'diagonal'

    def test_move_direction_diagonal_down(self):
        to_coords = self.coords(x=6, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'diagonal'

    def test_move_direction_horizontal(self):
        to_coords = self.coords(x=2, y=4)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'horizontal'

    def test_move_direction_horizontal(self):
        to_coords = self.coords(x=6, y=4)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'horizontal'

    def test_move_direction_vertical(self):
        to_coords = self.coords(x=4, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'vertical'

    def test_move_direction_vertical(self):
        to_coords = self.coords(x=4, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'vertical'

    def test_move_direction_non_linear(self):
        to_coords = self.coords(x=5, y=6)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'non_linear'

    def test_move_direction_non_linear(self):
        to_coords = self.coords(x=3, y=2)
        direction = move_direction(self.pawn, to_coords)
        assert direction == 'non_linear'
