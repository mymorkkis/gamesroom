"""Test module for game_errors."""
from collections import namedtuple
import unittest

from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


class GameErrorsTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.coords = namedtuple('Coords', 'x y')
        self.from_coords = self.coords(x=1, y=2)
        self.to_coords = self.coords(x=1, y=5)

    def test_invalid_move_error(self):
        err_msg = 'Invalid move for this piece'
        try:
            raise InvalidMoveError(self.from_coords, self.to_coords, err_msg)
        except InvalidMoveError as err:
            assert err.from_coords == self.from_coords
            assert err.to_coords == self.to_coords
            assert err.message == err_msg
        
    def test_not_on_board_error(self):
        err_msg = 'To_coordinates not valid board coordidnates'
        try:
            raise NotOnBoardError(self.to_coords, err_msg)
        except NotOnBoardError as err:
            assert err.coords == self.to_coords
            assert err.message == err_msg

    def test_piece_not_found_error(self):
        err_msg = 'No piece found at from_coordinates'
        try:
            raise PieceNotFoundError(self.from_coords, err_msg)
        except PieceNotFoundError as err:
            assert err.coords == self.from_coords
            assert err.message == err_msg
