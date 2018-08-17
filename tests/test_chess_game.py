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


@pytest.mark.parametrize('piece_type, value', [
    ('Rook', 2),
    ('Knight', 2),
    ('Bishop', 2),
    ('Queen', 1),
    ('King', 1),
    ('Pawn', 8),
    ('Rook', 2),
    ('Rook', 2),
])
def test_new_chess_game_has_correct_no_of_pieces(new_game, piece_type, value):
    for piece_color in (Color.WHITE, Color.BLACK):
        assert new_game.pieces[piece_color][piece_type] == value


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
    (Coords(x=1, y=2), None),   # all other squares contain None
    (Coords(x=3, y=3), None),
    (Coords(x=7, y=3), None),
    (Coords(x=2, y=4), None),
    (Coords(x=6, y=4), None),
    (Coords(x=7, y=5), None),
    (Coords(x=4, y=5), None), 
])
def test_new_chess_game_board_setup_correctly(new_game, coords, piece):
    assert new_game.board[coords.x][coords.y] == piece


# TODO Test game.restore() constructor


def test_piece_moved_on_board(game):
    add(Pawn(Color.WHITE), game.board, Coords(x=0, y=1), game.pieces)
    piece = game.board[0][1]
    # Move to postion is empty
    assert game.board[0][2] is None
    game.move(Coords(x=0, y=1), Coords(x=0, y=2))
    # Start position now empty
    assert game.board[0][1] is None
    # Move to postion now occupied and piece coordinates updated
    assert game.board[0][2] == Pawn(Color.WHITE)
    assert piece.coords.x == 0
    assert piece.coords.y == 2


def test_captured_piece_removed_from_board(game):
    add(Pawn(Color.WHITE), game.board, Coords(x=1, y=1), game.pieces)
    add(Pawn(Color.BLACK), game.board, Coords(x=2, y=2), game.pieces)
    opponent_piece = game.board[2][2]
    assert game.pieces[opponent_piece.color][opponent_piece.type] == 1
    # Attack opponent
    game.move(Coords(x=1, y=1), Coords(x=2, y=2))
    # Previous position empty
    assert game.board[1][1] is None
    # Captured piece removed and replaced by attacking piece
    assert game.board[2][2] == Pawn(Color.WHITE)
    # Captured piece no longer on board and removed from game pieces
    assert opponent_piece.coords is None
    assert game.pieces[opponent_piece.color][opponent_piece.type] == 0


def test_piece_blocking_move_raises_exception(game):
    add(Pawn(Color.WHITE), game.board, Coords(x=0, y=1), game.pieces)
    add(Pawn(Color.BLACK), game.board, Coords(x=0, y=2), game.pieces)
    print(game.board)
    with pytest.raises(InvalidMoveError):
        game.move(Coords(x=0, y=1), Coords(x=0, y=3))


def test_invalid_piece_move_raises_exception(game):
    add(Pawn(Color.WHITE), game.board, Coords(x=0, y=1), game.pieces)
    with pytest.raises(InvalidMoveError):
        # Pawn can't move horizontally
        game.move(Coords(x=0, y=1), Coords(x=1, y=1))
