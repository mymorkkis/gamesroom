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


@pytest.mark.parametrize('coords, opponent_piece, result', [
    (Coords(x=4, y=4), Bishop(Color.BLACK), True),
    (Coords(x=5, y=5), Queen(Color.BLACK), True),
    (Coords(x=1, y=3), Pawn(Color.BLACK), True),
    (Coords(x=3, y=3), Pawn(Color.BLACK), True),
    (Coords(x=2, y=1), King(Color.BLACK), True),
    (Coords(x=1, y=4), Knight(Color.BLACK), True),
    (Coords(x=4, y=3), Knight(Color.BLACK), True),
    (Coords(x=2, y=4), Rook(Color.BLACK), True),
    (Coords(x=4, y=2), Queen(Color.BLACK), True),
    (Coords(x=3, y=1), Queen(Color.BLACK), True),
    (Coords(x=0, y=0), Bishop(Color.BLACK), True),
    (Coords(x=0, y=2), Rook(Color.BLACK), True),
    # (Coords(x=0, y=2), Rook(Color.BLACK), False),
    # (Coords(x=0, y=2), Rook(Color.BLACK), False),
    # (Coords(x=0, y=2), Rook(Color.BLACK), False)
])
def test_king_in_check_returns_true(game, white_king, coords, opponent_piece, result):
    add(opponent_piece, game.board, coords, game.pieces)
    # King is at Coords(x=2, y=2)
    assert king_in_check(white_king.coords, game.board, opponent_color=opponent_piece.color) == result

# TODO test for black_king
