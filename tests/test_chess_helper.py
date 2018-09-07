"""Test module form chess_helper module."""
import pytest

from src.game_helper import add
from src.game_enums import Color
from src.chess_helper import chess_piece_blocking, king_in_check, new_chess_setup
from src.game_errors import InvalidMoveError
from src.game_helper import Coords, opponent_color_

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


def test_piece_blocking_diagonal_move_returns_true(game):
    # Test south/east and north/west
    add(Pawn(Color.WHITE), game, Coords(x=4, y=6))
    from_coords = Coords(x=7, y=3)
    to_coords = Coords(x=3, y=7)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=3, y=7)
    to_coords = Coords(x=7, y=3)
    assert chess_piece_blocking(game.board, from_coords, to_coords)

    # Test north/east and south/west
    add(Pawn(Color.WHITE), game, Coords(x=3, y=2))
    from_coords = Coords(x=1, y=0)
    to_coords = Coords(x=5, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=5, y=4)
    to_coords = Coords(x=1, y=0)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_horizontal_move_returns_true(game):
    add(Pawn(Color.WHITE), game, Coords(x=4, y=4))
    from_coords = Coords(x=2, y=4)
    to_coords = Coords(x=6, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=4)
    to_coords = Coords(x=2, y=4)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_vertical_move_returns_true(game):
    add(Pawn(Color.WHITE), game, Coords(x=4, y=4))
    from_coords = Coords(x=4, y=2)
    to_coords = Coords(x=4, y=6)
    assert chess_piece_blocking(game.board, from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=6)
    to_coords = Coords(x=4, y=2)
    assert chess_piece_blocking(game.board, from_coords, to_coords)


def test_piece_blocking_non_linear_move_returns_false(game):
    add(Pawn(Color.WHITE), game, Coords(x=4, y=4))
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
    add(king, game, Coords(x=2, y=2))
    add(opponent_piece, game, coords)
    assert king_in_check(king.coords, game.board, opponent_color_(king)) == result


def test_own_piece_blocks_king_being_in_check(game):
    king = King(Color.WHITE)
    blocking_piece = Pawn(Color.WHITE)
    opponent_piece = Queen(Color.BLACK)
    add(king, game, Coords(x=2, y=2))
    add(blocking_piece, game, Coords(x=3, y=3))
    add(opponent_piece, game, Coords(x=6, y=6))
    assert not king_in_check(king.coords, game.board, opponent_piece.color)


@pytest.mark.castle_tests
def test_white_king_can_castle_east(castle_game):
    castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))
    assert castle_game.board[6][0] == King(Color.WHITE)
    assert castle_game.board[5][0] == Rook(Color.WHITE)


@pytest.mark.castle_tests
def test_white_king_can_castle_west(castle_game):
    castle_game.move(Coords(x=4, y=0), Coords(x=2, y=0))
    assert castle_game.board[2][0] == King(Color.WHITE)
    assert castle_game.board[3][0] == Rook(Color.WHITE)


@pytest.mark.castle_tests
def test_black_king_can_castle_east(castle_game):
    castle_game.move(Coords(x=4, y=7), Coords(x=6, y=7))
    assert castle_game.board[6][7] == King(Color.BLACK)
    assert castle_game.board[5][7] == Rook(Color.BLACK)


@pytest.mark.castle_tests
def test_black_king_can_castle_west(castle_game):
    castle_game.move(Coords(x=4, y=7), Coords(x=2, y=7))
    assert castle_game.board[2][7] == King(Color.BLACK)
    assert castle_game.board[3][7] == Rook(Color.BLACK)


@pytest.mark.castle_tests
def test_cant_castle_if_king_already_moved(castle_game):
    castle_game.move(Coords(x=4, y=0), Coords(x=4, y=1))
    castle_game.move(Coords(x=4, y=1), Coords(x=4, y=0))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_rook_already_moved(castle_game):
    castle_game.move(Coords(x=7, y=0), Coords(x=7, y=1))
    castle_game.move(Coords(x=7, y=1), Coords(x=7, y=0))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_piece_blocking(castle_game):
    add(Bishop(Color.WHITE), castle_game, Coords(x=5, y=0))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_in_check(castle_game):
    add(Queen(Color.BLACK), castle_game, Coords(x=4, y=2))
    castle_game.board[4][0].in_check = True
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_moves_into_check(castle_game):
    add(Queen(Color.BLACK), castle_game, Coords(x=6, y=2))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_moves_through_check(castle_game):
    add(Queen(Color.BLACK), castle_game, Coords(x=5, y=2))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


# @pytest.mark.no_check_mate
@pytest.mark.parametrize('blocking_piece, coords', [
    (Pawn(Color.WHITE), Coords(x=2, y=1)),
    (Pawn(Color.WHITE), Coords(x=3, y=1)),
    (Rook(Color.WHITE), Coords(x=0, y=2)),
    (Rook(Color.WHITE), Coords(x=2, y=0)),
    (Bishop(Color.WHITE), Coords(x=0, y=2)),
    (Bishop(Color.WHITE), Coords(x=2, y=0)),
    (Knight(Color.WHITE), Coords(x=3, y=0)),
    (Knight(Color.WHITE), Coords(x=0, y=3)),
    (Queen(Color.WHITE), Coords(x=2, y=6)),
    (Queen(Color.WHITE), Coords(x=1, y=3))
])
def test_own_piece_can_block_check_mate(game, blocking_piece, coords):
    add(Queen(Color.BLACK), game, Coords(x=3, y=4))
    # White King is blocked in by own Pawn and Bishop
    add(Pawn(Color.WHITE), game, Coords(x=0, y=1))
    add(Bishop(Color.WHITE), game, Coords(x=1, y=0))
    # Blocking piece is in postion to block potential check mate
    add(blocking_piece, game, coords)
    # Queen moves to put king in check
    game.move(Coords(x=3, y=4), Coords(x=4, y=4))
    king = game.board[0][0]
    assert king.in_check
    # But not check mate as own piece can block
    assert not game.check_mate


@pytest.mark.no_check_mate
@pytest.mark.parametrize('attacking_piece, coords', [
    # (Pawn(Color.WHITE), Coords(x=3, y=3)),
    (Pawn(Color.WHITE), Coords(x=5, y=3)),
    (Rook(Color.WHITE), Coords(x=0, y=4)),
    (Rook(Color.WHITE), Coords(x=4, y=0)),
    (Bishop(Color.WHITE), Coords(x=5, y=3)),
    (Knight(Color.WHITE), Coords(x=3, y=2)),
    (Knight(Color.WHITE), Coords(x=0, y=3)),
    (Queen(Color.WHITE), Coords(x=4, y=0)),
    (Queen(Color.WHITE), Coords(x=3, y=5))
])
def test_own_piece_in_attack_position_stops_check_mate(game, attacking_piece, coords):
    add(Queen(Color.BLACK), game, Coords(x=3, y=4))
    # White King is blocked in by own Pawn and Bishop
    add(Pawn(Color.WHITE), game, Coords(x=0, y=1))
    add(Bishop(Color.WHITE), game, Coords(x=1, y=0))
    # Attacking piece is in postiton to take Queen when she moves
    add(attacking_piece, game, coords)
    # Queen moves to put king in check
    game.move(Coords(x=3, y=4), Coords(x=4, y=4))
    king = game.board[0][0]
    assert king.in_check
    # But not check mate as own piece can block
    assert not game.check_mate