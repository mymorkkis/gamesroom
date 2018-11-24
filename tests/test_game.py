"""Test module form game_helper module."""
import pytest

from src.game_enums import Color, Direction
from src.game import adjacent_squares, Coords, move_direction
from src.game_errors import IllegalMoveError, NotOnBoardError
from src.game_pieces.pawn import Pawn


@pytest.mark.parametrize('to_coords, direction', [
    (Coords(x=6, y=6), Direction.DIAGONAL),
    (Coords(x=2, y=2), Direction.DIAGONAL),
    (Coords(x=2, y=4), Direction.HORIZONTAL),
    (Coords(x=6, y=4), Direction.HORIZONTAL),
    (Coords(x=4, y=2), Direction.VERTICAL),
    (Coords(x=4, y=6), Direction.VERTICAL),
    (Coords(x=5, y=6), Direction.NON_LINEAR),
    (Coords(x=3, y=2), Direction.NON_LINEAR),
])
def test_move_direction_correct_for_coordinates(to_coords, direction):
    from_coords = Coords(x=4, y=4)
    assert move_direction(from_coords, to_coords) == direction


def test_same_from_and_to_coords_raise_exception(game):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=4)
    with pytest.raises(IllegalMoveError):
        game.validate_coords(from_coords, to_coords)


def test_no_piece_at_from_coords_raises_exception(game):
    from_coords = Coords(x=1, y=6)
    to_coords = Coords(x=1, y=5)
    with pytest.raises(IllegalMoveError):
        # No piece passed to function
        game.validate_coords(from_coords, to_coords)


# def test_attacking_piece_of_own_color_raises_exception(game):
#     game.add(Pawn(Color.WHITE), Coords(x=1, y=1))
#     with pytest.raises(IllegalMoveError):
#         # White king can't attack white Pawn
#         game.move(Coords(x=0, y=0), Coords(x=1, y=1))  # TODO rewrite the code for this

def test_adjacent_squares():
    assert not adjacent_squares(Coords(x=0, y=0), Coords(x=7, y=7))
    assert not adjacent_squares(Coords(x=0, y=0), Coords(x=2, y=2))
    assert adjacent_squares(Coords(x=0, y=0), Coords(x=1, y=1))
    assert adjacent_squares(Coords(x=0, y=0), Coords(x=0, y=1))
