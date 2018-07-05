"""Test module for Pawn game piece."""
from collections import namedtuple
import unittest

from src.chess_game import ChessGame
from src.game_errors import InvalidMoveError
from src.game_pieces.pawn import Pawn


class TestPawn(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.chess_game = ChessGame()
        self.coords = namedtuple('Coords', 'x y')
        self.start_coords = self.coords(x=6, y=3)
        self.black_pawn = Pawn(color='black')
        self.white_pawn = Pawn(color='white')

    def test_that_add_sets_x_coordinates(self):
        self.chess_game.add(self.black_pawn, self.start_coords)

        assert self.black_pawn.x_coord == 6

    def test_that_add_sets_y_coordinate(self):
        self.chess_game.add(self.black_pawn, self.start_coords)

        assert self.black_pawn.y_coord == 3

    def test_that_move_illegal_coords_right_does_not_move(self):
        to_coords = self.coords(x=7, y=3)
        self.chess_game.add(self.black_pawn, self.start_coords)

        self.assertRaises(InvalidMoveError, self.chess_game.move, self.start_coords, to_coords)
        assert self.black_pawn.x_coord == 6
        assert self.black_pawn.y_coord == 3

    def test_that_move_illegal_coords_left_does_not_move(self):
        to_coords = self.coords(x=4, y=3)
        self.chess_game.add(self.black_pawn, self.start_coords)

        self.assertRaises(InvalidMoveError, self.chess_game.move, self.start_coords, to_coords)
        assert self.black_pawn.x_coord == 6
        assert self.black_pawn.y_coord == 3


    def test_that_black_move_to_legal_coords_left_does_move(self):
        to_coords = self.coords(x=6, y=2)
        self.chess_game.add(self.black_pawn, self.start_coords)
        self.chess_game.move(self.start_coords, to_coords)

        assert self.black_pawn.x_coord == 6
        assert self.black_pawn.y_coord == 2

    def test_that_white_move_to_legal_coords_left_does_move(self):
        to_coords = self.coords(x=6, y=4)
        self.chess_game.add(self.white_pawn, self.start_coords)
        self.chess_game.move(self.start_coords, to_coords)
        
        assert self.white_pawn.x_coord == 6
        assert self.white_pawn.y_coord == 4
