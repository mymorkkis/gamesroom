"""Test module form chess_helper module."""
import pytest

from src.game_helper import add
from src.game_enums import Color
from src.game_helper import Coords
from src.chess_helper import chess_piece_blocking, king_in_check, new_chess_setup

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


CHESS_SETUP = new_chess_setup()


@pytest.mark.parametrize('key, piece', [
    ('00', Rook(Color.WHITE)),
    ('10', Knight(Color.WHITE)),
    ('20', Bishop(Color.WHITE)),
    ('30', Queen(Color.WHITE)),
    ('40', King(Color.WHITE)),
    ('50', Bishop(Color.WHITE)),
    ('60', Knight(Color.WHITE)),
    ('70', Rook(Color.WHITE)),
    ('01', Pawn(Color.WHITE)),
    ('11', Pawn(Color.WHITE)),
    ('21', Pawn(Color.WHITE)),
    ('31', Pawn(Color.WHITE)),
    ('41', Pawn(Color.WHITE)),
    ('51', Pawn(Color.WHITE)),
    ('61', Pawn(Color.WHITE)),
    ('71', Pawn(Color.WHITE)),
    ('06', Pawn(Color.BLACK)),
    ('16', Pawn(Color.BLACK)),
    ('26', Pawn(Color.BLACK)),
    ('36', Pawn(Color.BLACK)),
    ('46', Pawn(Color.BLACK)),
    ('56', Pawn(Color.BLACK)),
    ('66', Pawn(Color.BLACK)),
    ('76', Pawn(Color.BLACK)),
    ('07', Rook(Color.BLACK)),
    ('17', Knight(Color.BLACK)),
    ('27', Bishop(Color.BLACK)),
    ('37', Queen(Color.BLACK)),
    ('47', King(Color.BLACK)),
    ('57', Bishop(Color.BLACK)),
    ('67', Knight(Color.BLACK)),
    ('77', Rook(Color.BLACK)),
])
def test_new_chess_game_setup_correctly(key, piece):
    assert CHESS_SETUP[key] == piece


def test_piece_blocking_diagonal_move_returns_true(game, piece):
    # Piece at Coords(4, 4)
    from_coords = Coords(x=3, y=3)
    to_coords = Coords(x=6, y=6)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=6)
    to_coords = Coords(x=3, y=3)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_horizontal_move_returns_true(game, piece):
    # Piece at Coords(4, 4)
    from_coords = Coords(x=2, y=4)
    to_coords = Coords(x=6, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=4)
    to_coords = Coords(x=2, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_vertical_move_returns_true(game, piece):
    # Piece at Coords(4, 4)
    from_coords = Coords(x=4, y=2)
    to_coords = Coords(x=4, y=6)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=6)
    to_coords = Coords(x=4, y=2)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_non_linear_move_returns_false(game, piece):
    # Piece at Coords(4, 4)
    from_coords = Coords(x=3, y=3)
    to_coords = Coords(x=4, y=5)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=5)
    to_coords = Coords(x=3, y=3)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)


def test_no_piece_blocking_returns_false(game):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=6)
    assert not chess_piece_blocking(game.board, from_coords, to_coords)


@pytest.mark.parametrize('king, coords, opponent_piece, result', [
    (King(Color.WHITE), Coords(x=4, y=4), Bishop(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=5, y=5), Queen(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=1, y=3), Pawn(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=3, y=3), Pawn(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=2, y=1), King(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=1, y=4), Knight(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=4, y=3), Knight(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=2, y=4), Rook(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=4, y=2), Queen(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=3, y=1), Queen(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=0, y=0), Bishop(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=0, y=2), Rook(Color.BLACK), True),
    (King(Color.WHITE), Coords(x=7, y=7), Bishop(Color.WHITE), False),  # Own color doesn't put in check
    (King(Color.WHITE), Coords(x=0, y=2), Rook(Color.WHITE), False),    # Own color doesn't put in check
    (King(Color.WHITE), Coords(x=0, y=2), King(Color.BLACK), False),    # King over one square away can't put in check
    (King(Color.BLACK), Coords(x=1, y=1), Pawn(Color.WHITE), True),
    (King(Color.BLACK), Coords(x=3, y=1), Pawn(Color.WHITE), True)
])
def test_king_in_check_returns_correct_result(game, king, coords, opponent_piece, result):
    add(king, game.board, Coords(x=2, y=2), game.pieces)
    add(opponent_piece, game.board, coords, game.pieces)
    opponent_color = Color.WHITE if king.color == Color.BLACK else Color.BLACK
    assert king_in_check(king.coords, game.board, opponent_color) == result


def test_own_piece_blocks_king_being_in_check(game):
    king = King(Color.WHITE)
    blocking_piece = Pawn(Color.WHITE)
    opponent_piece = Queen(Color.BLACK)
    add(king, game.board, Coords(x=2, y=2), game.pieces)
    add(blocking_piece, game.board, Coords(x=3, y=3), game.pieces)
    add(opponent_piece, game.board, Coords(x=6, y=6), game.pieces)
    assert not king_in_check(king.coords, game.board, opponent_piece.color)
    