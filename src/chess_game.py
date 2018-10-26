from collections import defaultdict

from src.game_enums import Color, Direction
from src.game_errors import InvalidMoveError, NotOnBoardError, PieceNotFoundError
from src.game import Coords, Game

from src.game_pieces.bishop import Bishop
from src.game_pieces.king import King
from src.game_pieces.knight import Knight
from src.game_pieces.pawn import Pawn
from src.game_pieces.queen import Queen
from src.game_pieces.rook import Rook


class ChessGame(Game):
    """temp"""
    def __init__(self, restore_positions=None):
        super().__init__(
            board=[[None] * 8 for _ in range(8)],
            valid_piece_colors={Color.WHITE, Color.BLACK},
            valid_piece_names={'Bishop', 'King', 'Knight', 'Pawn', 'Queen', 'Rook'},
            pieces={
                Color.WHITE: defaultdict(int),
                Color.BLACK: defaultdict(int)
            },
            restore_positions=restore_positions
        )
        self.playing_color = Color.WHITE
        self.opponent_color = Color.BLACK
        # self.king_coords = {
        #     Color.WHITE: None,
        #     Color.BLACK: None
        # }
        # Move attributes
        self.from_coords = None
        self.to_coords = None
        self.playing_piece = None

        # self.check_mate = False

    @staticmethod
    def new_setup():
        """Return dictionary of new chess game default piece postitions.

        Dictionary is in following format:
        key = str representation of game coordinates xy
        value = chess GamePiece
        e.g '00': Rook(Color.WHITE)
        """
        white_pieces = chess_pieces(Color.WHITE, y_idxs=[0, 1])
        black_pieces = chess_pieces(Color.BLACK, y_idxs=[7, 6])
        return dict(white_pieces + black_pieces)

    def move(self, from_coords, to_coords):
        """temp"""

        self.validate_coords(from_coords, to_coords)
        self._set_move_attributes(from_coords, to_coords)
        legal_move, move_ = self._move_type()
        # is_legal, err_msg = is_legal_move()
        # if err_msg:
        #     raise InvalidMoveError(err_msg)
        # move_()
        if legal_move(to_coords) and not self.piece_blocking(from_coords, to_coords):
            if not self.own_king_in_check():
                move_()
                if self._check_mate():
                    self.winner = self.playing_color
                    # TODO End game
                self._switch_players()
            else:
                raise InvalidMoveError(from_coords, to_coords, 'Invalid move, King in check')
        else:
            raise InvalidMoveError(from_coords, to_coords, 'Invalid move for this piece')

    def _switch_players(self):
        playing_color = self.playing_color
        self.playing_color = self.opponent_color
        self.opponent_color = playing_color

    def _set_move_attributes(self, from_coords, to_coords):
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.playing_piece = self.board[from_coords.x][from_coords.y]

    def _move_type(self):
        if self._castle_move():
            return self._legal_castle, self._castle_move_type()
        if self._prawn_promotion():
            return self.playing_piece.valid_move, self._promote_pawn
        if self._capture_move():
            return self.playing_piece.valid_capture, self._capture
        return self.playing_piece.valid_move, self._move

    def piece_blocking(self, from_coords, to_coords):
        """Check if any piece blocking move from_coords to_coords. Return bool."""
        if self.move_direction(from_coords, to_coords) != Direction.NON_LINEAR:
            # Only Knights move non_linear and they can jump over pieces
            for coords in self.coords_between(from_coords, to_coords):
                if self.board[coords.x][coords.y] is not None:
                    return True
        return False

    def _promote_pawn(self):
        self.board[self.from_coords.x][self.from_coords.y] = None
        # Defaults to Queen as most players want this
        # TODO Add functionality to choose promotion piece
        self.board[self.to_coords.x][self.to_coords.y] = Queen(self.playing_color)

    def _move(self):
        self.board[self.from_coords.x][self.from_coords.y] = None
        self.playing_piece.coords = self.to_coords
        self.board[self.to_coords.x][self.to_coords.y] = self.playing_piece

    def _capture(self):
        captured_piece = self.board[self.to_coords.x][self.to_coords.y]
        captured_piece.coords = None
        self.pieces[captured_piece.color][captured_piece.name] -= 1
        self.board[self.from_coords.x][self.from_coords.y] = None
        self.board[self.to_coords.x][self.to_coords.y] = self.playing_piece

    def _castle_move(self):
        if self.playing_piece.name == 'King' and self.playing_piece.color == Color.WHITE:
            if (self.from_coords == Coords(4, 0)
                    and self.to_coords in (Coords(2, 0), Coords(6, 0))):
                return True
        if self.playing_piece.name == 'King' and self.playing_piece.color == Color.BLACK:
            if (self.from_coords == Coords(4, 7)
                    and self.to_coords in (Coords(2, 7), Coords(6, 7))):
                return True
        return False

    def _castle_move_type(self):
        if self.to_coords.y == 0:
            if self.to_coords.x == 2:
                return self._legal_castle, self._white_castle_queen_side
            return self._legal_castle, self._white_castle_king_side
        if self.to_coords.y == 7:
            if self.to_coords.x == 2:
                return self._legal_castle, self._black_castle_queen_side
            return self._legal_castle, self._black_castle_king_side

    def _prawn_promotion(self):
        return self.playing_piece.name == 'Pawn' and self.to_coords.y in (0, 7)

    def _legal_castle(self, to_coords):
        color, side, castle_coords = self._castle_info(to_coords)

        if self._king_moved(color) or self._rook_moved(color, side):
            return False

        for coords in castle_coords:
            if (self.board[coords.x][coords.y] is not None
                    or self._king_in_check(coords)):
                return False
        return True

    def _castle_info(self, to_coords):
        castle_coords = [self.from_coords]

        if to_coords.y == 0:
            color = Color.WHITE
            if to_coords.x == 2:
                side = 'Queen'
                castle_coords.extend([Coords(x=3, y=0), Coords(x=2, y=0)])
            if to_coords.x == 6:
                side = 'King'
                castle_coords.extend([Coords(x=5, y=0), Coords(x=6, y=0)])
        if to_coords.y == 7:
            color = Color.BLACK
            if to_coords.x == 2:
                side = 'Queen'
                castle_coords.extend([Coords(x=3, y=7), Coords(x=2, y=7)])
            if to_coords.x == 6:
                side = 'King'
                castle_coords.extend([Coords(x=5, y=7), Coords(x=6, y=7)])

        return color, side, castle_coords

    def _king(self, color):
        for row in self.board:
            for piece in row:
                if piece and piece.name == 'King' and piece.color == color:
                    return piece

    def _king_moved(self, color):
        king = self._king(color)
        return king.moved

    def _rook_moved(self, color, side):
        if color == Color.WHITE:
            if side == 'King':
                piece = self.board[7][0]
            if side == 'Queen':
                piece = self.board[0][0]
        if color == Color.BLACK:
            if side == 'King':
                piece = self.board[7][7]
            if side == 'Queen':
                piece = self.board[0][7]

        return not piece or piece.name != 'Rook' or piece.color != color or piece.moved

    def _legal_en_passant(self):
        # check last move was opponent pawn moving 2 spaces
        pass

    def _white_castle_king_side(self):
        self.board[4][0], self.board[7][0] = None, None
        self.board[6][0], self.board[5][0] = self._king_rook_castled_pieces(Color.WHITE)

    def _white_castle_queen_side(self):
        self.board[4][0], self.board[0][0] = None, None
        self.board[2][0], self.board[3][0] = self._king_rook_castled_pieces(Color.WHITE)

    def _black_castle_king_side(self):
        self.board[4][7], self.board[7][7] = None, None
        self.board[6][7], self.board[5][7] = self._king_rook_castled_pieces(Color.BLACK)

    def _black_castle_queen_side(self):
        self.board[4][7], self.board[0][7] = None, None
        self.board[2][7], self.board[3][7] = self._king_rook_castled_pieces(Color.BLACK)

    @staticmethod
    def _king_rook_castled_pieces(playing_color):
        king, rook = King(playing_color), Rook(playing_color)
        king.moved = True
        rook.moved = True
        return king, rook

    def _capture_move(self):
        return self.board[self.to_coords.x][self.to_coords.y] is not None or self._en_passant()

    def _en_passant(self):
        if (self.playing_piece.name == 'Pawn' and self.playing_piece.valid_capture(self.to_coords)
                and self.board[self.to_coords.x][self.to_coords.y] is None):
            if self.playing_piece.color == Color.WHITE and self.to_coords.y == 5:
                return self.board[self.to_coords.x][self.to_coords.y - 1] == Pawn(Color.BLACK)
            if self.playing_piece.color == Color.BLACK and self.to_coords.y == 2:
                return self.board[self.to_coords.x][self.to_coords.y + 1] == Pawn(Color.WHITE)
        return False

    def own_king_in_check(self):
        """Check if move puts current player king in check. Return bool."""
        # Keep track of current game state
        king = self._king(self.playing_color)
        original_king_coords = king.coords
        original_piece = self.board[self.to_coords.x][self.to_coords.y]

        # Temporarily change to future board position to see if it will lead to check
        self.board[self.from_coords.x][self.from_coords.y] = None
        self.board[self.to_coords.x][self.to_coords.y] = self.playing_piece
        if self.playing_piece.name == 'King':
            king.coords = self.to_coords

        # Perform check evaluation
        in_check = True if self._king_in_check(king.coords) else False

        # Return game to previous state
        self.board[self.from_coords.x][self.from_coords.y] = self.playing_piece
        self.board[self.to_coords.x][self.to_coords.y] = original_piece
        king.coords = original_king_coords

        return in_check

    def _check_mate(self):
        # king_coords = self.king_coords[self.opponent_color]
        king = self._king(self.opponent_color)
        # if king_can_move
        if self._can_attack_attacking_piece():
            return False
        if self._piece_can_block_capture(king.coords):
            return False
        return True

    def _can_attack_attacking_piece(self):
        for piece in self._board_pieces(self.playing_color):
            if (piece.valid_capture(self.to_coords)
                    and not self.piece_blocking(piece.coords, self.to_coords)):
                return True
        return False

    def _king_in_check(self, coords):
        # king_coords = self.king_coords[self.opponent_color]
        king = self._king(self.opponent_color)

        for piece in self._board_pieces(self.opponent_color):
            if piece.valid_capture(coords) and not self.piece_blocking(piece.coords, king.coords):
                return True
        return False

    def _piece_can_block_capture(self, king_coords):
        pieces = self._board_pieces(self.playing_color, king_wanted=False)
        for coords in self.coords_between(self.to_coords, king_coords):
            for piece in pieces:
                if piece.valid_move(self.to_coords) and not self.piece_blocking(piece.coords, coords):
                    return True
        return False

    def _board_pieces(self, color, king_wanted=True):
        king = None if king_wanted else 'King'

        return [piece for row in self.board for piece in row
                if piece and piece.color == color and piece.name != king]

def chess_pieces(color, *, y_idxs=None):
    """Helper method for new_chess_setup."""
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
