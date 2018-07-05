"""Test module form ChessBoard class."""
from collections import namedtuple
import unittest

from src.chess_game import ChessGame
from src.game_pieces.pawn import Pawn
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError


class ChessGameTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

        self.pawn = Pawn(color='black')
        self.chess_game = ChessGame()
        self.coords = namedtuple('Coords', 'x y')
        self.move = self.chess_game.move
        # Pretend Pawns are generic pieces for testing 'piece blocking move' raises error
        self.piece = Pawn(color='black')
        self.blocking_piece = Pawn(color='black')

    def test_has_max_board_width_of_8(self):
        assert self.chess_game.MAX_BOARD_HEIGHT == 8

    def test_has_max_board_height_of_8(self):
        assert self.chess_game.MAX_BOARD_WIDTH == 8

    def test_lower_left_corner_is_valid_position(self):
        coords = self.coords(x=0, y=0)
        assert self.chess_game._legal_board_position(coords)

    def test_upper_right_corner_is_valid_position(self):
        coords = self.coords(x=7, y=7)
        assert self.chess_game._legal_board_position(coords)

    def test_position_out_of_bounds_east_is_invalid(self):
        coords = self.coords(x=11, y=5)
        assert not self.chess_game._legal_board_position(coords)

    def test_position_out_of_bounds_north_is_invalid(self):
        coords = self.coords(x=5, y=9)
        assert not self.chess_game._legal_board_position(coords)

    def test_that_avoids_duplicate_positioning(self):
        second_pawn = Pawn(color='black')
        coords = self.coords(x=6, y=3)
        self.chess_game.add(self.pawn, coords)
        self.chess_game.add(second_pawn, coords)

        assert self.pawn.x_coord == 6
        assert self.pawn.y_coord == 3
        assert not second_pawn.x_coord
        assert not second_pawn.y_coord

    def test_limits_the_number_of_pawns(self):
        for count in range(10):
            pawn = Pawn(color='black')
            row = count / self.chess_game.MAX_BOARD_WIDTH
            x_coord = count
            y_coord = count % self.chess_game.MAX_BOARD_WIDTH
            self.chess_game.add(
                pawn,
                self.coords(x=x_coord, y=y_coord)
            )

            if row < 1:
                assert pawn.x_coord == count
                assert pawn.y_coord == count % self.chess_game.MAX_BOARD_WIDTH
            else:
                assert not pawn.x_coord
                assert not pawn.y_coord

    def test_piece_moved_on_board(self):
        self.chess_game.add(self.pawn, self.coords(x=6, y=6))
        self.chess_game.move(self.coords(x=6, y=6), self.coords(x=6, y=5))

        # Previous positon empty
        assert self.chess_game.board[6][6] is None
        # New postion occupied and Pawn coordinates updated
        assert self.chess_game.board[6][5] == self.pawn
        assert self.pawn.x_coord == 6
        assert self.pawn.y_coord == 5

        self.chess_game.move(self.coords(x=6, y=5), self.coords(x=6, y=4))

        # Previous position empty
        assert self.chess_game.board[6][5] is None
        # New postion occupied and Pawn coordinates updated
        assert self.chess_game.board[6][4] == self.pawn
        assert self.pawn.x_coord == 6
        assert self.pawn.y_coord == 4

    def test_captured_piece_removed_from_board(self):
        white_pawn1 = Pawn(color='white')       
        white_pawn2 = Pawn(color='white')
        color = white_pawn2.color
        type_ = white_pawn2.type       
        self.chess_game.add(self.pawn, self.coords(x=6, y=6))
        self.chess_game.add(white_pawn1, self.coords(x=5, y=5))
        self.chess_game.add(white_pawn2, self.coords(x=4, y=4))

        assert white_pawn1.x_coord == 5
        assert white_pawn1.y_coord == 5       
        assert self.chess_game.pieces[color][type_] == 2
        # Attack white_pawn1
        self.chess_game.move(self.coords(x=6, y=6), self.coords(x=5, y=5))
        # Previous position empty
        assert self.chess_game.board[6][6] is None
        # Captured piece removed and replaced by attacking piece
        assert self.chess_game.board[5][5] == self.pawn
        assert self.pawn.x_coord == 5
        assert self.pawn.y_coord == 5
        # Captured piece no longer on board
        assert not white_pawn1.x_coord
        assert not white_pawn1.x_coord
        assert self.chess_game.pieces[color][type_] == 1

        assert white_pawn2.x_coord == 4
        assert white_pawn2.y_coord == 4       
        # Attack white_pawn2
        self.chess_game.move(self.coords(x=5, y=5), self.coords(x=4, y=4))
        # Previous position empty
        assert self.chess_game.board[5][5] is None
        # Captured piece removed and replaced by attacking piece
        assert self.chess_game.board[4][4] == self.pawn
        assert self.pawn.x_coord == 4
        assert self.pawn.y_coord == 4
        # Captured piece no longer on board
        assert not white_pawn2.x_coord
        assert not white_pawn2.x_coord
        assert self.chess_game.pieces[color][type_] == 0

    def test_invalid_from_coords_raises_exception(self):
        from_coords = self.coords(x=1, y=50)
        to_coords = self.coords(x=1, y=6)
        self.assertRaises(NotOnBoardError, self.move, from_coords, to_coords)

    def test_invalid_to_coords_raises_exception(self):
        from_coords = self.coords(x=1, y=6)
        to_coords = self.coords(x=50, y=7)
        self.assertRaises(NotOnBoardError, self.move, from_coords, to_coords)

    def test_empty_from_coords_raises_exception(self):
        from_coords = self.coords(x=1, y=6)
        to_coords = self.coords(x=1, y=5)
        self.assertRaises(PieceNotFoundError, self.move, from_coords, to_coords)

    def test_same_from_and_to_coords_raise_exception(self):
        self.chess_game.add(self.piece, self.coords(1, 2))
        from_coords = self.coords(x=1, y=2)
        to_coords = self.coords(x=1, y=2)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)       

    def test_piece_blocking_vertical_move_raises_exception(self):
        self.chess_game.add(self.piece, self.coords(2, 2))
        self.chess_game.add(self.blocking_piece, self.coords(2, 3))
        from_coords = self.coords(2, 2)
        to_coords = self.coords(2, 4)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)

    def test_piece_blocking_vertical_move_down_raises_exception(self):
        self.chess_game.add(self.piece, self.coords(2, 6))
        self.chess_game.add(self.blocking_piece, self.coords(2, 4))
        from_coords = self.coords(2, 6)
        to_coords = self.coords(2, 2)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)

    def test_piece_blocking_horizontal_move_raises_exception(self):
        self.chess_game.add(self.piece, self.coords(2, 2))
        self.chess_game.add(self.blocking_piece, self.coords(4, 2))
        from_coords = self.coords(2, 2)
        to_coords = self.coords(5, 2)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)
    
    def test_piece_blocking_diagonal_move_raises_exception(self):
        self.chess_game.add(self.piece, self.coords(1, 2))
        self.chess_game.add(self.blocking_piece, self.coords(3, 4))
        from_coords = self.coords(1, 2)
        to_coords = self.coords(4, 5)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)

    def test_piece_blocking_diagonal_down_move_raises_exception(self):
        self.chess_game.add(self.piece, self.coords(6, 7))
        self.chess_game.add(self.blocking_piece, self.coords(3, 4))
        from_coords = self.coords(6, 7)
        to_coords = self.coords(1, 2)
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)
  
    def test_invalid_move_for_piece_raises_exception(self):
        from_coords = self.coords(x=1, y=2)
        to_coords = self.coords(x=2, y=2)
        self.chess_game.add(self.pawn, from_coords)
        # Pawn cant move horizontal
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)

    def test_invalid_capture_for_piece_raises_exception(self):
        from_coords = self.coords(x=1, y=6)
        to_coords = self.coords(x=1, y=5)
        self.chess_game.add(self.pawn, from_coords)
        self.chess_game.add(self.piece, to_coords)
        # Pawn cant capture vertically
        self.assertRaises(InvalidMoveError, self.move, from_coords, to_coords)
