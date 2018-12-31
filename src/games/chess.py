"""Contains Chess class."""
from copy import deepcopy

from src.game_enums import ChessPiece, Color, Direction
from src.game_errors import IllegalMoveError
from src.games.game import Coords, Game, move_direction, NEXT_ADJACENT_COORD, TWO_COORD_ERR_MSG

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


class Chess(Game):
    """Contains logic for Chess."""

    ILLEGAL_MOVE = 'Illegal move for piece'
    ILLEGAL_CAPTURE = 'Illegal capture for piece'
    ILLEGAL_CASTLE = 'Illegal castle move attempted'
    ILLEGAL_EN_PASSANT = 'Illegal en passant attempted'
    KING_IN_CHECK = 'Must move king out of check'
    OWN_PIECE_ATTACK = 'Cannot attack own piece'
    PIECE_BLOCKING = 'Piece blocking attempted move'
    CASTLE_IN_CHECK = 'Cannot castle out of, through or into check'


    def __init__(self, restore_positions=None):

        CHESS_SETUP = {
            'board': [[None] * 8 for _ in range(8)],
            'legal_piece_colors': {Color.WHITE, Color.BLACK},
            'legal_piece_names': {piece.value for piece in ChessPiece},
            'start_color': Color.WHITE,
            'input_err_msg': TWO_COORD_ERR_MSG
        }

        super().__init__(CHESS_SETUP, restore_positions)

        self.last_move_pawn = None  # Used for checking legality of en passant attempt

    def make_move(self):
        self._raise_errors_if_chess_specific_illegal_move()

        make_move, legal_move, error_message = self._move_type()

        if legal_move(self.to_coords):
            make_move()
            if self._check_mate():
                self.winner = self.playing_color.value
            self.switch_players()
        else:
            raise IllegalMoveError(error_message)

    def _move_type(self):
        if self._castle_move():
            return (self._castle_move_type(),
                    self._legal_castle,
                    self.ILLEGAL_CASTLE)
        if self._prawn_promotion():
            return (self._promote_pawn,
                    self.playing_piece.legal_move,
                    self.ILLEGAL_MOVE)
        if self._en_passant():
            return (self._capture_en_passant,
                    self._legal_en_passant,
                    self.ILLEGAL_EN_PASSANT)
        if self._capture_move():
            return (self._move,
                    self.playing_piece.legal_capture,
                    self.ILLEGAL_CAPTURE)
        return (self._move,
                self.playing_piece.legal_move,
                self.ILLEGAL_MOVE)

    def _piece_blocking(self, from_coords, to_coords):
        if move_direction(from_coords, to_coords) != Direction.NON_LINEAR:
            # Only Knights move non_linear and they can jump over pieces
            for coords in self.coords_between(from_coords, to_coords):
                if self.board[coords.x][coords.y] is not None:
                    return True
        return False

    def _promote_pawn(self):
        self.board[self.from_coords.x][self.from_coords.y] = None
        # Defaults to Queen as most players want this
        # TODO Add functionality to choose promotion piece
        promoted_piece = Queen(self.playing_color)
        promoted_piece.coords = self.to_coords
        self.board[self.to_coords.x][self.to_coords.y] = promoted_piece

    def _move(self):
        self._move_piece_and_update_coords()

        if self._pawn_two_space_first_move():
            self.last_move_pawn = self.playing_piece
        else:
            self.last_move_pawn = None

        if self.playing_piece in [King(self.playing_color), Rook(self.playing_color)]:
            self.playing_piece.moved = True

    def _raise_errors_if_chess_specific_illegal_move(self):
        captured_piece = self.board[self.to_coords.x][self.to_coords.y]

        if captured_piece and captured_piece.color == self.playing_color:
            raise IllegalMoveError(self.OWN_PIECE_ATTACK)

        if self._piece_blocking(self.from_coords, self.to_coords):
            raise IllegalMoveError(self.PIECE_BLOCKING)

        if self._own_king_in_check():
            if self._castle_move():
                raise IllegalMoveError(self.CASTLE_IN_CHECK)
            raise IllegalMoveError(self.KING_IN_CHECK)

    def _pawn_two_space_first_move(self):
        if (self.playing_piece == Pawn(Color.WHITE)
                and self.from_coords.y == 1 and self.to_coords.y == 3):
            return True
        if (self.playing_piece == Pawn(Color.BLACK)
                and self.from_coords.y == 6 and self.to_coords.y == 4):
            return True
        return False

    def _capture_en_passant(self):
        coords = self.last_move_pawn.coords
        captured_piece = self.board[coords.x][coords.y]
        captured_piece.coords = None
        self.board[coords.x][coords.y] = None
        self._move()

    def _castle_move(self):
        if self.playing_piece == King(Color.WHITE):
            if (self.from_coords == Coords(4, 0)
                    and self.to_coords in (Coords(2, 0), Coords(6, 0))):
                return True
        if self.playing_piece == King(Color.BLACK):
            if (self.from_coords == Coords(4, 7)
                    and self.to_coords in (Coords(2, 7), Coords(6, 7))):
                return True
        return False

    def _castle_move_type(self):
        if self._white_king_row():
            return self._white_castle()
        if self._black_king_row():
            return self._black_castle()

    def _white_king_row(self):
        return self.to_coords.y == 0

    def _black_king_row(self):
        return self.to_coords.y == 7

    def _king_side(self):
        return self.to_coords.x == 6

    def _queen_side(self):
        return self.to_coords.x == 2

    def _white_castle(self):
        if self._queen_side():
            return self._white_castle_queen_side
        return self._white_castle_king_side

    def _black_castle(self):
        if self._queen_side():
            return self._black_castle_queen_side
        return self._black_castle_king_side

    def _prawn_promotion(self):
        return (self.playing_piece == Pawn(Color.WHITE) and self._black_king_row()
                or self.playing_piece == Pawn(Color.BLACK) and self._white_king_row())

    def _legal_castle(self, to_coords=None):
        playing_color = self.playing_color
        move_coords = self._castle_coords()

        if (self._king_moved(playing_color) or self._rook_moved(playing_color)
                or self._king_in_check(playing_color, self.from_coords)):
            return False

        for coords in move_coords:
            if (self.board[coords.x][coords.y] is not None
                    or self._king_in_check(playing_color, coords)):
                return False
        return True

    def _castle_coords(self):
        if self._white_king_row():
            if self._queen_side():
                castle_coords = (Coords(x=3, y=0), Coords(x=2, y=0))
            if self._king_side():
                castle_coords = (Coords(x=5, y=0), Coords(x=6, y=0))
        if self._black_king_row():
            if self._queen_side():
                castle_coords = (Coords(x=3, y=7), Coords(x=2, y=7))
            if self._king_side():
                castle_coords = (Coords(x=5, y=7), Coords(x=6, y=7))
        return castle_coords

    def _king(self, wanted_color):
        for piece in self.current_board_pieces():
            if piece == King(wanted_color):
                return piece

    def _king_moved(self, playing_color):
        king = self._king(playing_color)
        return king.moved

    def _rook_moved(self, playing_color):
        if playing_color == Color.WHITE:
            if self._king_side():
                piece = self.board[7][0]
            if self._queen_side():
                piece = self.board[0][0]

        if playing_color == Color.BLACK:
            if self._king_side():
                piece = self.board[7][7]
            if self._queen_side():
                piece = self.board[0][7]

        return piece and piece == Rook(playing_color) and piece.moved

    def _legal_en_passant(self, to_coords):
        if not self.last_move_pawn:
            return False
        if self.playing_piece == Pawn(Color.WHITE) and to_coords.y == 5:
            return Coords(to_coords.x, to_coords.y - 1) == self.last_move_pawn.coords
        if self.playing_piece == Pawn(Color.BLACK) and to_coords.y == 2:
            return Coords(to_coords.x, to_coords.y + 1) == self.last_move_pawn.coords
        return False

    def _white_castle_king_side(self):
        king, rook = self.board[4][0], self.board[7][0]
        self.board[4][0], self.board[7][0] = None, None
        self.board[6][0], self.board[5][0] = king, rook
        king.moved, rook.moved = True, True

    def _white_castle_queen_side(self):
        king, rook = self.board[4][0], self.board[0][0]
        self.board[4][0], self.board[0][0] = None, None
        self.board[2][0], self.board[3][0] = king, rook
        king.moved, rook.moved = True, True

    def _black_castle_king_side(self):
        king, rook = self.board[4][7], self.board[7][7]
        self.board[4][7], self.board[7][7] = None, None
        self.board[6][7], self.board[5][7] = king, rook
        king.moved, rook.moved = True, True

    def _black_castle_queen_side(self):
        king, rook = self.board[4][7], self.board[0][7]
        self.board[4][7], self.board[0][7] = None, None
        self.board[2][7], self.board[3][7] = king, rook
        king.moved, rook.moved = True, True

    def _capture_move(self):
        return self.board[self.to_coords.x][self.to_coords.y] is not None

    def _en_passant(self):
        if (self.playing_piece == Pawn(self.playing_color)
                and self.playing_piece.legal_capture(self.to_coords)
                and self.board[self.to_coords.x][self.to_coords.y] is None
                and self._potential_en_passant_capture_piece()):
            return True
        return False

    def _potential_en_passant_capture_piece(self):
        y_coord = self.to_coords.y - 1 if self.playing_color == Color.WHITE else self.to_coords.y + 1
        if self.board[self.to_coords.x][y_coord] == Pawn(self.opponent_color):
            return True
        return False

    def _own_king_in_check(self):
        """Check if move will put/keep current player king in check. Return bool."""
        cloned_game = deepcopy(self)
        cloned_game.board[self.from_coords.x][self.from_coords.y] = None
        cloned_game.board[self.to_coords.x][self.to_coords.y] = self.playing_piece

        king = cloned_game._king(self.playing_color)
        king_coords = self.to_coords if king == self.playing_piece else king.coords

        return cloned_game._king_in_check(self.playing_color, king_coords)

    def _check_mate(self):
        king = self._king(self.opponent_color)

        if not self._king_in_check(king.color, king.coords):
            return False
        if self._king_can_move_out_of_attack(king.coords):
            return False
        if self._can_attack_attacking_piece():
            return False
        if self._piece_can_block_attack(king.coords):
            return False
        return True

    def _king_in_check(self, king_color, king_coords):
        opponent_color = Color.WHITE if king_color == Color.BLACK else Color.BLACK

        for piece in self._board_pieces(opponent_color):
            if (piece.legal_capture(king_coords)
                    and not self._piece_blocking(piece.coords, king_coords)):
                return True
        return False

    def _king_can_move_out_of_attack(self, king_coords):
        for square_coords in self._adjacent_empty_square_coords(king_coords):
            if not self._king_in_check(self.playing_color, square_coords):
                return True
        return False

    def _can_attack_attacking_piece(self):
        for piece in self._board_pieces(self.opponent_color):
            if (piece.legal_capture(self.to_coords)
                    and not self._piece_blocking(piece.coords, self.to_coords)):
                return True
        return False

    def _piece_can_block_attack(self, king_coords):
        pieces = self._board_pieces(self.opponent_color, king_wanted=False)
        for coords in self.coords_between(self.to_coords, king_coords):
            for piece in pieces:
                if (piece.legal_move(coords)
                        and not self._piece_blocking(piece.coords, coords)):
                    return True
        return False

    def _board_pieces(self, color, king_wanted=True):
        king = None if king_wanted else King(color)

        return [piece for piece in self.current_board_pieces()
                if piece.color == color and piece != king]

    def _adjacent_empty_square_coords(self, king_coords):
        potential_coords = [adjacent_coord(king_coords)
                            for adjacent_coord
                            in NEXT_ADJACENT_COORD.values()]

        return [coords for coords in potential_coords
                if self.coords_on_board(coords)
                and self.board[coords.x][coords.y] is None]

    @staticmethod
    def _new_board_setup():
        white_pieces = chess_pieces(Color.WHITE, y_idxs=[0, 1])
        black_pieces = chess_pieces(Color.BLACK, y_idxs=[7, 6])
        return dict(white_pieces + black_pieces)


def chess_pieces(color, *, y_idxs=None):
    """Helper function for new Chess setup.

       Return list of [start_coords, pieces] for given color
    """
    coords = [f'{x_idx}{y_idx}' for y_idx in y_idxs for x_idx in range(8)]
    pieces = [
        Rook(color),
        Knight(color),
        Bishop(color),
        Queen(color),
        King(color),
        Bishop(color),
        Knight(color),
        Rook(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color),
        Pawn(color)
    ]
    return list(zip(coords, pieces))
