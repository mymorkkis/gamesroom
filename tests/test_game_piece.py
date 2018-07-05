"""Test module for GamePieces ABC."""
import unittest

from src.game_pieces.game_piece import GamePiece
from src.game_pieces.pawn import Pawn


class TestGamePiece(unittest.TestCase):

    def test_that_game_piece_cant_be_instantiated(self):
        self.assertRaises(TypeError, GamePiece)

    def test_that_child_class_inherits_properties(self):
        pawn = Pawn(color='black')
        test_repr = "Pawn('black')"
        test_str = 'Black Pawn: x_coord = None, y_coord = None'

        assert pawn.type == 'Pawn'
        assert repr(pawn) == test_repr
        assert str(pawn) == test_str

    def test_that_abstract_methods_require_implementing(self):
        class TestPiece(GamePiece):
            def move():
                pass

        # No capture method
        self.assertRaises(TypeError, TestPiece)

        class TestPiece(GamePiece):
            def capture():
                pass

        # No move method 
        self.assertRaises(TypeError, TestPiece)
