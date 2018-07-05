"""Test module for Queen game piece."""
from collections import namedtuple
import unittest

from src.chess_game import ChessGame
from src.game_pieces.queen import Queen

class TestQueen(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.chess_game = ChessGame()
        self.queen = Queen(color='black')
        self.coords = namedtuple('Coords', 'x y')
        self.start_coords = self.coords(x=7, y=4)
        self.chess_game.add(self.queen, self.start_coords)

    def test_horizontal_move_valid(self):
        valid = self.queen.valid_move(self.coords(x=1, y=4))
        assert valid

    def test_vertical_capture_valid(self):
        valid = self.queen.valid_capture(self.coords(x=7, y=6))
        assert valid

    def test_diagonal_move_valid(self):
        valid = self.queen.valid_move(self.coords(x=5, y=2))
        assert valid

    def test_nonlinear_move_not_valid(self):
        valid = self.queen.valid_move(self.coords(x=1, y=5))
        assert not valid

    def test_nonlinear_capture_not_valid(self):
        valid = self.queen.valid_move(self.coords(x=6, y=2))
        assert not valid
