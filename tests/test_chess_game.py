"""Test module form ChessGame class."""
import pytest

from src.game_enums import Color
from src.game import Coords
from src.game_errors import InvalidMoveError

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


@pytest.mark.parametrize('piece_name, value', [
    ('Rook', 2),
    ('Knight', 2),
    ('Bishop', 2),
    ('Queen', 1),
    ('King', 1),
    ('Pawn', 8),
    ('Rook', 2),
    ('Rook', 2)
])
def test_new_chess_game_has_correct_no_of_pieces(new_game, piece_name, value):
    for piece_color in (Color.WHITE, Color.BLACK):
        assert new_game.pieces[piece_color][piece_name] == value


@pytest.mark.parametrize('coords, piece', [
    (Coords(x=0, y=0), Rook(Color.WHITE)),
    (Coords(x=1, y=0), Knight(Color.WHITE)),
    (Coords(x=2, y=0), Bishop(Color.WHITE)),
    (Coords(x=3, y=0), Queen(Color.WHITE)),
    (Coords(x=4, y=0), King(Color.WHITE)),
    (Coords(x=5, y=0), Bishop(Color.WHITE)),
    (Coords(x=6, y=0), Knight(Color.WHITE)),
    (Coords(x=7, y=0), Rook(Color.WHITE)),
    (Coords(x=0, y=1), Pawn(Color.WHITE)),
    (Coords(x=1, y=1), Pawn(Color.WHITE)),
    (Coords(x=2, y=1), Pawn(Color.WHITE)),
    (Coords(x=3, y=1), Pawn(Color.WHITE)),
    (Coords(x=4, y=1), Pawn(Color.WHITE)),
    (Coords(x=5, y=1), Pawn(Color.WHITE)),
    (Coords(x=6, y=1), Pawn(Color.WHITE)),
    (Coords(x=7, y=1), Pawn(Color.WHITE)),
    (Coords(x=0, y=6), Pawn(Color.BLACK)),
    (Coords(x=1, y=6), Pawn(Color.BLACK)),
    (Coords(x=2, y=6), Pawn(Color.BLACK)),
    (Coords(x=3, y=6), Pawn(Color.BLACK)),
    (Coords(x=4, y=6), Pawn(Color.BLACK)),
    (Coords(x=5, y=6), Pawn(Color.BLACK)),
    (Coords(x=6, y=6), Pawn(Color.BLACK)),
    (Coords(x=7, y=6), Pawn(Color.BLACK)),
    (Coords(x=0, y=7), Rook(Color.BLACK)),
    (Coords(x=1, y=7), Knight(Color.BLACK)),
    (Coords(x=2, y=7), Bishop(Color.BLACK)),
    (Coords(x=3, y=7), Queen(Color.BLACK)),
    (Coords(x=4, y=7), King(Color.BLACK)),
    (Coords(x=5, y=7), Bishop(Color.BLACK)),
    (Coords(x=6, y=7), Knight(Color.BLACK)),
    (Coords(x=7, y=7), Rook(Color.BLACK)),
    (Coords(x=4, y=2), None),   # Random selection of coords to show
    (Coords(x=1, y=2), None),   # that all other squares contain None
    (Coords(x=3, y=3), None),
    (Coords(x=7, y=3), None),
    (Coords(x=2, y=4), None),
    (Coords(x=6, y=4), None),
    (Coords(x=7, y=5), None),
    (Coords(x=4, y=5), None)
])
def test_new_chess_game_board_setup_correctly(new_game, coords, piece):
    assert new_game.board[coords.x][coords.y] == piece


def test_piece_moved_on_board(game):
    game.add(Pawn(Color.WHITE), Coords(x=0, y=1))
    # Move to postion is empty
    assert game.board[0][2] is None
    game.move(Coords(x=0, y=1), Coords(x=0, y=2))
    # Start position now empty
    assert game.board[0][1] is None
    # Move_to postion now_ occupied and piece coordinates updated
    piece = game.board[0][2]
    assert piece == Pawn(Color.WHITE)
    assert piece.coords.x == 0
    assert piece.coords.y == 2


def test_captured_piece_removed_from_board(game):
    game.add(Pawn(Color.WHITE), Coords(x=1, y=1))
    game.add(Pawn(Color.BLACK), Coords(x=2, y=2))
    opponent_piece = game.board[2][2]
    assert game.pieces[opponent_piece.color][opponent_piece.name] == 1
    # Attack opponent
    game.move(Coords(x=1, y=1), Coords(x=2, y=2))
    # Previous position empty
    assert game.board[1][1] is None
    # Captured piece removed and replaced by attacking piece
    assert game.board[2][2] == Pawn(Color.WHITE)
    # Captured piece no longer on board and removed from game pieces
    assert opponent_piece.coords is None
    assert game.pieces[opponent_piece.color][opponent_piece.name] == 0


def test_piece_blocking_move_raises_exception(game):
    game.add(Pawn(Color.WHITE), Coords(x=0, y=1))
    game.add(Pawn(Color.BLACK), Coords(x=0, y=2))
    with pytest.raises(InvalidMoveError):
        game.move(Coords(x=0, y=1), Coords(x=0, y=3))


def test_invalid_piece_move_raises_exception(game):
    game.add(Pawn(Color.WHITE), Coords(x=0, y=1))
    with pytest.raises(InvalidMoveError):
        # Pawn can't move horizontally
        game.move(Coords(x=0, y=1), Coords(x=1, y=1))


def test_king_moving_into_check_raises_exception(game):
    game.add(Rook(Color.WHITE), Coords(x=6, y=1))
    with pytest.raises(InvalidMoveError):
        game.move(Coords(x=7, y=7), Coords(x=6, y=7))


def test_move_putting_own_king_in_check_raises_exception(game):
    game.add(Rook(Color.BLACK), Coords(x=7, y=6))
    game.add(Rook(Color.WHITE), Coords(x=7, y=1))
    game.playing_color = Color.BLACK
    with pytest.raises(InvalidMoveError):
        # Moving black Rook leaves King exposed to white Rook
        game.move(Coords(x=7, y=6), Coords(x=6, y=6))


def test_not_moving_king_out_of_check_raises_exception(game):
    game.add(Rook(Color.WHITE), Coords(x=7, y=1))
    with pytest.raises(InvalidMoveError):
        # King moves but remains in check
        game.move(Coords(x=7, y=7), Coords(x=7, y=6))


def test_white_pawn_can_be_promoted_to_queen(game):
    game.add(Pawn(Color.WHITE), Coords(x=2, y=6))
    assert game.pieces[Color.WHITE]['Queen'] == 0
    assert game.pieces[Color.WHITE]['Pawn'] == 1
    game.move(Coords(x=2, y=6), Coords(x=2, y=7))
    # White Pawn promoted to white Queen
    assert game.pieces[Color.WHITE]['Queen'] == 1
    assert game.pieces[Color.WHITE]['Pawn'] == 0
    assert game.board[2][7] == Queen(Color.WHITE)


def test_black_pawn_can_be_promoted_to_queen(game):
    game.add(Pawn(Color.BLACK), Coords(x=2, y=1))
    assert game.pieces[Color.BLACK]['Queen'] == 0
    assert game.pieces[Color.BLACK]['Pawn'] == 1
    game.playing_color = Color.BLACK
    game.move(Coords(x=2, y=1), Coords(x=2, y=0))
    # Black Pawn promoted to Black Queen
    assert game.pieces[Color.BLACK]['Queen'] == 1
    assert game.pieces[Color.BLACK]['Pawn'] == 0
    assert game.board[2][0] == Queen(Color.BLACK)


def test_piece_blocking_diagonal_move_returns_true(game):
    # Test south/east and north/west
    game.add(Pawn(Color.WHITE), Coords(x=4, y=6))
    from_coords = Coords(x=7, y=3)
    to_coords = Coords(x=3, y=7)
    assert game._piece_blocking(from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=3, y=7)
    to_coords = Coords(x=7, y=3)
    assert game._piece_blocking(from_coords, to_coords)

    # Test north/east and south/west
    game.add(Pawn(Color.WHITE), Coords(x=3, y=2))
    from_coords = Coords(x=1, y=0)
    to_coords = Coords(x=5, y=4)
    assert game._piece_blocking(from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=5, y=4)
    to_coords = Coords(x=1, y=0)
    assert game._piece_blocking(from_coords, to_coords)


def test_piece_blocking_horizontal_move_returns_true(game):
    game.add(Pawn(Color.WHITE), Coords(x=4, y=4))
    from_coords = Coords(x=2, y=4)
    to_coords = Coords(x=6, y=4)
    assert game._piece_blocking(from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=6, y=4)
    to_coords = Coords(x=2, y=4)
    assert game._piece_blocking(from_coords, to_coords)


def test_piece_blocking_vertical_move_returns_true(game):
    game.add(Pawn(Color.WHITE), Coords(x=4, y=4))
    from_coords = Coords(x=4, y=2)
    to_coords = Coords(x=4, y=6)
    assert game._piece_blocking(from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=6)
    to_coords = Coords(x=4, y=2)
    assert game._piece_blocking(from_coords, to_coords)


def test_piece_blocking_non_linear_move_returns_false(game):
    game.add(Pawn(Color.WHITE), Coords(x=4, y=4))
    from_coords = Coords(x=3, y=3)
    to_coords = Coords(x=4, y=5)
    assert not game._piece_blocking(from_coords, to_coords)
    # Assert test works in both directions
    from_coords = Coords(x=4, y=5)
    to_coords = Coords(x=3, y=3)
    assert not game._piece_blocking(from_coords, to_coords)


def test_no_piece_blocking_returns_false(game):
    from_coords = Coords(x=4, y=4)
    to_coords = Coords(x=4, y=6)
    assert not game._piece_blocking(from_coords, to_coords)


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
    # TODO rewrite this test, feels messy
    game.board[0][0] = None
    game.add(king, Coords(x=2, y=2))
    game.add(opponent_piece, coords)
    game.playing_color = opponent_piece.color
    game.opponent_color = king.color
    assert game._king_in_check(king.color, king.coords) == result


def test_own_piece_blocks_king_being_in_check(game):
    king = King(Color.WHITE)
    blocking_piece = Pawn(Color.WHITE)
    opponent_piece = Queen(Color.BLACK)
    game.add(king, Coords(x=2, y=2))
    game.add(blocking_piece, Coords(x=3, y=3))
    game.add(opponent_piece, Coords(x=6, y=6))
    assert not game._king_in_check(king.color, king.coords)


def test_king_moved_is_recorded(castle_game):
    king = castle_game.board[4][0]
    assert not king.moved
    castle_game.move(king.coords, Coords(x=4, y=1))
    assert king.moved


def test_rook_moved_is_recorded(castle_game):
    rook = castle_game.board[0][0]
    assert not rook.moved
    castle_game.move(rook.coords, Coords(x=0, y=1))
    assert rook.moved


@pytest.mark.castle_tests
def test_white_king_can_castle_king_side(castle_game):
    castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))
    assert castle_game.board[6][0] == King(Color.WHITE)
    assert castle_game.board[5][0] == Rook(Color.WHITE)


@pytest.mark.castle_tests
def test_white_king_can_castle_queen_side(castle_game):
    castle_game.move(Coords(x=4, y=0), Coords(x=2, y=0))
    assert castle_game.board[2][0] == King(Color.WHITE)
    assert castle_game.board[3][0] == Rook(Color.WHITE)


@pytest.mark.castle_tests
def test_black_king_can_castle_king_side(castle_game):
    castle_game.playing_color = Color.BLACK
    castle_game.move(Coords(x=4, y=7), Coords(x=6, y=7))
    assert castle_game.board[6][7] == King(Color.BLACK)
    assert castle_game.board[5][7] == Rook(Color.BLACK)


@pytest.mark.castle_tests
def test_black_king_can_castle_queen_side(castle_game):
    castle_game.playing_color = Color.BLACK
    castle_game.move(Coords(x=4, y=7), Coords(x=2, y=7))
    assert castle_game.board[2][7] == King(Color.BLACK)
    assert castle_game.board[3][7] == Rook(Color.BLACK)


@pytest.mark.castle_tests
def test_cant_castle_if_king_already_moved(castle_game):
    king = castle_game.board[4][0]
    king.moved = True
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_rook_already_moved(castle_game):
    rook = castle_game.board[7][0]
    rook.moved = True
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if__piece_blocking(castle_game):
    castle_game.add(Bishop(Color.WHITE), Coords(x=5, y=0))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_in_check(castle_game):
    castle_game.add(Queen(Color.BLACK), Coords(x=4, y=2))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_moves_into_check(castle_game):
    castle_game.add(Queen(Color.BLACK), Coords(x=6, y=2))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


@pytest.mark.castle_tests
def test_cant_castle_if_king_moves_through_check(castle_game):
    castle_game.add(Queen(Color.BLACK), Coords(x=5, y=2))
    with pytest.raises(InvalidMoveError):
        castle_game.move(Coords(x=4, y=0), Coords(x=6, y=0))


# @pytest.mark.no_check_mate
# @pytest.mark.parametrize('blocking_piece, coords', [
#     (Pawn(Color.WHITE), Coords(x=2, y=1)),
#     (Pawn(Color.WHITE), Coords(x=3, y=1)),
#     (Rook(Color.WHITE), Coords(x=0, y=2)),
#     (Rook(Color.WHITE), Coords(x=2, y=0)),
#     (Bishop(Color.WHITE), Coords(x=0, y=2)),
#     (Bishop(Color.WHITE), Coords(x=2, y=0)),
#     (Knight(Color.WHITE), Coords(x=3, y=0)),
#     (Knight(Color.WHITE), Coords(x=0, y=3)),
#     (Queen(Color.WHITE), Coords(x=2, y=6)),
#     (Queen(Color.WHITE), Coords(x=1, y=3))
# ])
# def test_own_piece_can_block_check_mate(game, blocking_piece, coords):
#     game.add(Queen(Color.BLACK), Coords(x=3, y=4))
#     # White King is blocked in by own Pawn and Bishop
#     game.add(Pawn(Color.WHITE), Coords(x=0, y=1))
#     game.add(Bishop(Color.WHITE), Coords(x=1, y=0))
#     # Blocking piece is in postion to block potential check mate
#     game.add(blocking_piece, coords)
#     # Queen moves to put king in check
#     game.move(Coords(x=3, y=4), Coords(x=4, y=4))
#     king = game.board[0][0]
#     assert king.in_check
#     # But not check mate as own piece can block
#     assert not game.check_mate


# @pytest.mark.no_check_mate
# @pytest.mark.parametrize('attacking_piece, coords', [
#     # (Pawn(Color.WHITE), Coords(x=3, y=3)),
#     (Pawn(Color.WHITE), Coords(x=5, y=3)),
#     (Rook(Color.WHITE), Coords(x=0, y=4)),
#     (Rook(Color.WHITE), Coords(x=4, y=0)),
#     (Bishop(Color.WHITE), Coords(x=5, y=3)),
#     (Knight(Color.WHITE), Coords(x=3, y=2)),
#     (Knight(Color.WHITE), Coords(x=0, y=3)),
#     (Queen(Color.WHITE), Coords(x=4, y=0)),
#     (Queen(Color.WHITE), Coords(x=3, y=5))
# ])
# def test_own_piece_in_attack_position_stops_check_mate(game, attacking_piece, coords):
#     game.add(Queen(Color.BLACK), Coords(x=3, y=4))
#     # White King is blocked in by own Pawn and Bishop
#     game.add(Pawn(Color.WHITE), Coords(x=0, y=1))
#     game.add(Bishop(Color.WHITE), Coords(x=1, y=0))
#     # Attacking piece is in postiton to take Queen when she moves
#     game.add(attacking_piece, coords)
#     # Queen moves to put king in check
#     game.move(Coords(x=3, y=4), Coords(x=4, y=4))
#     king = game.board[0][0]
#     assert king.in_check
#     # But not check mate as own piece can block
#     assert not game.check_mate


# @pytest.mark.no_check_mate
# def test_king_can_attack_out_of_check_mate(game):
#     game.add(Queen(Color.BLACK), Coords(x=1, y=4))
#     game.move(Coords(x=1, y=4), Coords(x=1, y=1))
#     king = game.board[0][0]
#     assert king.in_check
#     # But not check mate as King can attack Queen
#     assert not game.check_mate


# @pytest.mark.no_check_mate
# def test_king_can_escape_out_of_check_mate(game):
#     game.add(Rook(Color.BLACK), Coords(x=1, y=4))
#     game.add(Bishop(Color.BLACK), Coords(x=2, y=1))
#     game.move(Coords(x=1, y=4), Coords(x=1, y=0))
#     king = game.board[0][0]
#     assert king.in_check
#     # But not check mate as King escape (can't attack Rook as Bishop is protecting)
#     assert not game.check_mate


# def test_checkmate_results_in_game_ending(new_game):
#     game = new_game
#     # Setup classic "fool's mate"
#     game.move(Coords(x=5, y=1), Coords(x=5, y=2))
#     game.move(Coords(x=4, y=6), Coords(x=4, y=4))
#     game.move(Coords(x=6, y=1), Coords(x=6, y=3))
#     # assert not game.check_mate
#     assert not game.winner
#     # Queen to put king in check mate
#     game.move(Coords(x=3, y=7), Coords(x=7, y=3))
#     # assert game.check_mate
#     assert game.winner == Color.BLACK