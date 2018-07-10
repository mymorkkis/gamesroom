"""Test module form ChessGame class."""
from collections import defaultdict
import pytest

from src.chess_game import ChessGame
from src.game_enums import Color
from src.game_helper import Coords
from src.game_pieces.pawn import Pawn
from src.game_errors import InvalidMoveError, NotOnBoardError


@pytest.fixture(scope='function')
def game():
    chess_game = ChessGame()
    return chess_game


@pytest.fixture(scope='function')
def piece():
    white_piece = Pawn(Color.WHITE)
    return white_piece


@pytest.fixture(scope='function')
def opponent_piece():
    black_piece = Pawn(Color.BLACK)
    return black_piece


def test_chess_game_initialized_correctly(game):
    assert game.BOARD_HEIGHT == 8
    assert game.BOARD_WIDTH == 8
    assert game.MAX_PIECES == {
        'Pawn': 8,
        'Knight': 2,
        'Bishop': 2,
        'Rook': 2,
        'Queen': 1,
        'King': 1
    }
    assert game.board == [[None] * 8 for _ in range(8)]
    assert game.pieces == {
        Color.WHITE: defaultdict(int),
        Color.BLACK: defaultdict(int)
    }


def test_piece_added_to_board(game, piece):
    game.add(piece, Coords(x=0, y=1))
    assert game.board[0][1] == piece
    assert piece.x_coord == 0
    assert piece.y_coord == 1
    assert game.pieces[piece.color][piece.type] == 1


def test_multiple_pieces_not_added_to_same_board_position(game, piece):
    game.add(piece, Coords(x=0, y=1))
    piece2 = Pawn(Color.WHITE)
    game.add(piece2, Coords(x=0, y=1))
    assert piece2.x_coord is None
    assert piece2.y_coord is None
    assert game.pieces[piece2.color][piece2.type] == 1


def test_piece_not_added_at_ilegal_coordinates(game, piece):
    with pytest.raises(NotOnBoardError):
        game.add(piece, Coords(x=10, y=10))
    assert piece.x_coord is None
    assert piece.y_coord is None
    assert game.pieces[piece.color][piece.type] == 0


def test_pieces_dont_pass_max_quantity(game, piece):
    # 8 Pawns allowed per color
    for y_coordinate in range(8):
        x_coord = 2
        y_coord = y_coordinate
        game.add(piece, Coords(x=x_coord, y=y_coord))
    assert game.pieces[piece.color][piece.type] == 8
    # No more Pawns accepted
    game.add(piece, Coords(x=3, y=0))  
    assert game.pieces[piece.color][piece.type] == 8


def test_piece_moved_on_board(game, piece):
    game.add(piece, Coords(x=0, y=1))
    assert game.board[0][1] == piece
    game.move(Coords(x=0, y=1), Coords(x=0, y=2))
    # Previous positon empty
    assert game.board[0][1] is None
    # New postion occupied and piece coordinates updated
    assert game.board[0][2] == piece
    assert piece.x_coord == 0
    assert piece.y_coord == 2


def test_captured_piece_removed_from_board(game, piece, opponent_piece):
    game.add(piece, Coords(x=0, y=1))
    game.add(opponent_piece, Coords(x=1, y=2))
    assert game.pieces[opponent_piece.color][opponent_piece.type] == 1
    # Attack opponent
    game.move(Coords(x=0, y=1), Coords(x=1, y=2))
    # Previous position empty
    assert game.board[0][1] is None
    # Captured piece removed and replaced by attacking piece
    assert game.board[1][2] == piece
    # Captured piece no longer on board
    assert opponent_piece.x_coord is None
    assert opponent_piece.y_coord is None
    assert game.pieces[opponent_piece.color][opponent_piece.type] == 0


def test_piece_blocking_move_raises_exception(game, piece, opponent_piece):
    game.add(piece, Coords(x=0, y=1))
    game.add(opponent_piece, Coords(x=0, y=2))
    with pytest.raises(InvalidMoveError):
        game.move(Coords(x=0, y=1), Coords(x=0, y=3))


def test_invalid_piece_move_raises_exception(game, piece):
    game.add(piece, Coords(x=0, y=1))
    with pytest.raises(InvalidMoveError):
        # Pawn can't move horizontally
        game.move(Coords(x=0, y=1), Coords(x=1, y=1))
