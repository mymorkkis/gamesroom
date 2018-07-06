"""Test module for GamePieces ABC."""
import pytest

from src.game_enums import Color
from src.game_pieces.game_piece import GamePiece
from src.game_pieces.pawn import Pawn


def test_game_piece_cant_be_instantiated():
    with pytest.raises(TypeError):
        game_piece = GamePiece()


def test_child_class_inherits_properties():
    pawn = Pawn(Color.BLACK)
    test_repr = "Pawn(<Color.BLACK: 2>)"
    test_str = 'Black Pawn: x_coord = None, y_coord = None'

    assert pawn.type == 'Pawn'
    assert pawn.color == Color.BLACK
    assert pawn.x_coord is None
    assert pawn.y_coord is None
    assert repr(pawn) == test_repr
    assert str(pawn) == test_str


def test_invalid_game_color_throws_error():
    with pytest.raises(AttributeError):
        Pawn(Color.GREY)

    with pytest.raises(ValueError):
        Pawn('white')


def test_abstract_methods_require_implementing():
    # No capture method
    class TestPiece(GamePiece):
        def move():
            pass

    with pytest.raises(TypeError):
        TestPiece()

    # No move method
    class TestPiece(GamePiece):
        def capture():
            pass

    with pytest.raises(TypeError):
        TestPiece()
