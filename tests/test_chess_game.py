"""Test module form ChessGame class."""
import pytest

from src.game_enums import Color
from src.game_helper import add, Coords
from src.game_errors import InvalidMoveError

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


# @pytest.mark.parametrize('piece_name, value', [
#     ('Rook', 2),
#     ('Knight', 2),
#     ('Bishop', 2),
#     ('Queen', 1),
#     ('King', 1),
#     ('Pawn', 8),
#     ('Rook', 2),
#     ('Rook', 2)
# ])
# def test_new_chess_game_has_correct_no_of_pieces(new_game, piece_name, value):
#     for piece_color in (Color.WHITE, Color.BLACK):
#         assert new_game.pieces[piece_color][piece_name] == value


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


# def test_piece_moved_on_board(game):
#     add(Pawn(Color.WHITE), game, Coords(x=0, y=1))
#     # Move to postion is empty
#     assert game.board[0][2] is None
#     game.move(Coords(x=0, y=1), Coords(x=0, y=2))
#     # Start position now empty
#     assert game.board[0][1] is None
#     # Move_to postion now_ occupied and piece coordinates updated
#     piece = game.board[0][2]
#     assert piece == Pawn(Color.WHITE)
#     assert piece.coords.x == 0
#     assert piece.coords.y == 2


# def test_captured_piece_removed_from_board(game):
#     add(Pawn(Color.WHITE), game, Coords(x=1, y=1))
#     add(Pawn(Color.BLACK), game, Coords(x=2, y=2))
#     opponent_piece = game.board[2][2]
#     assert game.pieces[opponent_piece.color][opponent_piece.name] == 1
#     # Attack opponent
#     game.move(Coords(x=1, y=1), Coords(x=2, y=2))
#     # Previous position empty
#     assert game.board[1][1] is None
#     # Captured piece removed and replaced by attacking piece
#     assert game.board[2][2] == Pawn(Color.WHITE)
#     # Captured piece no longer on board and removed from game pieces
#     assert opponent_piece.coords is None
#     assert game.pieces[opponent_piece.color][opponent_piece.name] == 0


# def test_piece_blocking_move_raises_exception(game):
#     add(Pawn(Color.WHITE), game, Coords(x=0, y=1))
#     add(Pawn(Color.BLACK), game, Coords(x=0, y=2))
#     with pytest.raises(InvalidMoveError):
#         game.move(Coords(x=0, y=1), Coords(x=0, y=3))


# def test_invalid_piece_move_raises_exception(game):
#     add(Pawn(Color.WHITE), game, Coords(x=0, y=1))
#     with pytest.raises(InvalidMoveError):
#         # Pawn can't move horizontally
#         game.move(Coords(x=0, y=1), Coords(x=1, y=1))


# def test_game_king_coords_updated_when_king_moved(game):
#     game.move(Coords(x=0, y=0), Coords(x=0, y=1))
#     assert game.king_coords[Color.WHITE] == Coords(x=0, y=1)


# def test_opponent_king_put_in_check(game):
#     king = game.board[7][7]
#     add(Rook(Color.WHITE), game, Coords(x=6, y=1))
#     assert not king.in_check
#     game.move(Coords(x=6, y=1), Coords(x=7, y=1))
#     assert king.in_check


# def test_king_moving_into_check_raises_exception(game):
#     add(Rook(Color.WHITE), game, Coords(x=6, y=1))
#     with pytest.raises(InvalidMoveError):
#         game.move(Coords(x=7, y=7), Coords(x=6, y=7))


# def test_move_putting_own_king_in_check_raises_exception(game):
#     add(Rook(Color.BLACK), game, Coords(x=7, y=6))
#     add(Rook(Color.WHITE), game, Coords(x=7, y=1))
#     with pytest.raises(InvalidMoveError):
#         # Moving black Rook leaves King exposed to white Rook
#         game.move(Coords(x=7, y=6), Coords(x=6, y=6))


# def test_not_moving_king_out_of_check_raises_exception(game):
#     add(Rook(Color.WHITE), game, Coords(x=7, y=1))
#     with pytest.raises(InvalidMoveError):
#         # King moves but remains in check
#         game.move(Coords(x=7, y=7), Coords(x=7, y=6))


# def test_move_blocks_king_being_in_check(game):
#     add(Rook(Color.BLACK), game, Coords(x=6, y=6))
#     king = game.board[7][7]
#     add(Rook(Color.WHITE), game, Coords(x=7, y=1))
#     king.in_check = True
#     game.move(Coords(x=6, y=6), Coords(x=7, y=6))
#     assert not king.in_check


# def test_king_can_move_out_of_check(game):
#     king = game.board[7][7]
#     add(Rook(Color.WHITE), game, Coords(x=7, y=1))
#     king.in_check = True
#     game.move(Coords(x=7, y=7), Coords(x=6, y=7))
#     assert not king.in_check


# def test_checkmate_results_in_game_ending(new_game):
#     game = new_game
#     # Setup classic "fool's mate"
#     game.move(Coords(x=5, y=1), Coords(x=5, y=2))
#     game.move(Coords(x=4, y=6), Coords(x=4, y=4))
#     game.move(Coords(x=6, y=1), Coords(x=6, y=3))
#     assert not game.check_mate
#     assert not game.winner
#     # Queen to put king in check mate
#     game.move(Coords(x=3, y=7), Coords(x=7, y=3))
#     assert game.check_mate
#     assert game.winner == Color.BLACK


# def test_white_pawn_can_be_promoted_to_queen(game):
#     add(Pawn(Color.WHITE), game, Coords(x=2, y=6))
#     assert game.pieces[Color.WHITE]['Queen'] == 0
#     assert game.pieces[Color.WHITE]['Pawn'] == 1
#     game.move(Coords(x=2, y=6), Coords(x=2, y=7))
#     # White Pawn promoted to white Queen
#     assert game.pieces[Color.WHITE]['Queen'] == 1
#     assert game.pieces[Color.WHITE]['Pawn'] == 0
#     assert game.board[2][7] == Queen(Color.WHITE)

# def test_black_pawn_can_be_promoted_to_queen(game):
#     add(Pawn(Color.BLACK), game, Coords(x=2, y=1))
#     assert game.pieces[Color.BLACK]['Queen'] == 0
#     assert game.pieces[Color.BLACK]['Pawn'] == 1
#     game.move(Coords(x=2, y=1), Coords(x=2, y=0))
#     # Black Pawn promoted to Black Queen
#     assert game.pieces[Color.BLACK]['Queen'] == 1
#     assert game.pieces[Color.BLACK]['Pawn'] == 0
#     assert game.board[2][0] == Queen(Color.BLACK)
