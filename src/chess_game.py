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
        super().__init__()
        self.board = [[None] * 8 for _ in range(8)]
        self.board_width = len(self.board[0])
        self.board_height = len(self.board)
        self.playing_color = Color.WHITE
        self.opponent_color = Color.BLACK
        self.pieces = {
            Color.WHITE: defaultdict(int),
            Color.BLACK: defaultdict(int)
        }
        self.valid_piece_names = {'Bishop', 'King', 'Knight', 'Pawn', 'Queen', 'Rook'}
        self.valid_piece_colors = {Color.WHITE, Color.BLACK}
        self.king_coords = {
            Color.WHITE: None,
            Color.BLACK: None
        }
        self._setup_game(restore_positions)
        self.from_coords = None
        self.to_coords = None
        self.playing_piece = None
        self.from_board_position = None
        self.to_board_position = None

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
        self._set_move_attibutes(from_coords, to_coords)
        # move_type = _move_type(from_coords, to_coords)
        is_legal_move, move_ = self._move_type()
        # is_legal, err_msg = is_legal_move()
        # if err_msg:
        #     raise InvalidMoveError(err_msg)
        # move_()
        if is_legal_move(self.board, from_coords, to_coords):
            if not self.own_king_in_check():
                move_(self.board, from_coords, to_coords)
                if self._check_mate():
                    pass
                    # TODO End game
                self._switch_players()

    def _setup_game(self, game_positions):
        """Setup board for new or previously stored game."""
        if game_positions is None:
            game_positions = self.new_setup()

        for coords, piece in game_positions.items():
            assert piece.color in self.valid_piece_colors
            assert piece.name in self.valid_piece_names
            coords = Coords(x=int(coords[0]), y=int(coords[1]))
            self.add(piece, coords)
            if piece.name == 'King':
                self.king_coords[piece.color] = piece.coords

    def add(self, piece, coords):
        """Add piece on board at given coordinates and update piece coordinates. Increment pieces.
        (Chess only): Add King coordinates to king_coords dictionary.
        Args:
                piece:  Any piece that inherits from GamePiece
                game:   Game object
                coords: Namedtuple with coordinates x & y. E.g. Coords(x=0, y=1).
        Raises:
                NotOnBoardError
        """
        try:
            self.board[coords.x][coords.y] = piece
            piece.coords = coords
            self.pieces[piece.color][piece.name] += 1

        except IndexError:
            raise NotOnBoardError(coords, 'Saved coordinates are not valid coordinates')

    def coords_on_board(self, x_coord, y_coord):
        """Check if coordinates within board range (negative indexing not allowed). Return bool."""
        return 0 <= x_coord < self.board_width and 0 <= y_coord < self.board_height

    def _switch_players(self):
        playing_color = self.playing_color
        self.playing_color = self.opponent_color
        self.opponent_color = playing_color


    def _set_move_attibutes(self, from_coords, to_coords):
        self.from_coords, self.to_coords = from_coords, to_coords
        self.playing_piece = self.board[from_coords.x][from_coords.y]
        self.from_board_position = self.board[from_coords.x][from_coords.y]
        self.to_board_position = self.board[to_coords.x][to_coords.y]

    def _move_type(self):
        if self._castle_move():
            return self._legal_castle, self._castle_move_type()
        if self._prawn_promotion():
            return self.playing_piece.valid_move, self._promote_pawn
        if self._attack_move():
            return self.playing_piece.valid_attack, self._attack
        return self.playing_piece.valid_move, self._move

    def piece_blocking(self, from_coords, to_coords):
        """Check if any piece blocking move from_coords to_coords. Return bool."""
        if self.move_direction(self.from_coords, self.to_coords) != Direction.NON_LINEAR:
            # Only Knights move non_linear and they can jump over pieces
            for coords in self.coords_between(from_coords, to_coords):
                if self.board[coords.x][coords.y] is not None:
                    return True
        return False

    def _promote_pawn(self):
        self.from_board_position = None
        # Defaults to Queen as most players want this
        # TODO Add functionality to choose promotion piece
        self.to_board_position = Queen(self.playing_color)

    def _move(self):
        self.from_board_position = None
        self.to_board_position = self.playing_piece

    def _attack(self):
        self.from_board_position = None
        captured_piece = self.to_board_position
        captured_piece.coords = None
        # self.pieces[captured_piece.color][captured_piece.name] -= 1
        self.to_board_position = self.playing_piece

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
                return (self._legal_castle(Color.WHITE, side='Queen'),
                        self._white_castle_queen_side)
            return self._white_castle_king_side
        if self.to_coords.y == 7:
            if self.to_coords.x == 2:
                return self._black_castle_queen_side
            return self._black_castle_king_side

    def _prawn_promotion(self):
        return self.playing_piece.name == 'Pawn' and self.to_coords.y in (0, 7)

    def _legal_castle(self, color, side):
        if self._king_moved(color) or self._rook_moved(color, side):
            return False

        for coords in self._castle_coords(color, side):
            if (self.board[coords.x][coords.y] is not None
                    or self._king_in_check(coords)):
                return False
        return True

    def _castle_coords(self, color, side):
        if color == Color.WHITE:
            if side == 'King':
                move_thru, move_to = Coords(x=5, y=0), Coords(x=6, y=0)
            if side == 'Queen':
                move_thru, move_to = Coords(x=3, y=0), Coords(x=2, y=0)
        if color == Color.BLACK:
            if side == 'King':
                move_thru, move_to = Coords(x=5, y=7), Coords(x=6, y=7)
            if side == 'Queen':
                move_thru, move_to = Coords(x=3, y=7), Coords(x=2, y=7)
        return self.from_coords, move_thru, move_to

    def _king_moved(self, color):
        king_coords = self.king_coords[color]
        king = self.board[king_coords.x][king_coords.y]
        return king or king.moved

    def _rook_moved(self, color, side):
        if color == Color.WHITE:
            if side == 'King':
                rook = self.board[7][0]
                if not rook or rook.moved:
                    return False
            if side == 'Queen':
                rook = self.board[0][0]
                if not rook or rook.moved:
                    return False
        if color == Color.BLACK:
            if side == 'King':
                rook = self.board[7][7]
                if not rook or rook.moved:
                    return False
            if side == 'Queen':
                rook = self.board[0][7]
                if not rook or rook.moved:
                    return False

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

    def _attack_move(self):
        return self.to_board_position is not None or self._en_passant()

    def _en_passant(self):
        if (self.playing_piece.name == 'Pawn' and self.playing_piece.valid_capture(self.to_coords)
                and self.to_board_position is None):
            if self.playing_piece.color == Color.WHITE and self.to_coords.y == 5:
                return self.board[self.to_coords.x][self.to_coords.y - 1] == Pawn(Color.BLACK)
            if self.playing_piece.color == Color.BLACK and self.to_coords.y == 2:
                return self.board[self.to_coords.x][self.to_coords.y + 1] == Pawn(Color.WHITE)
        return False

    def own_king_in_check(self):
        """Check if move puts current player king in check. Return bool."""
        # TODO Needs completing
        # Keep track of current game state
        original_piece = self.playing_piece
        original_king_coords = self.king_coords[self.playing_color]

        # Temporarily change to future board position to see if it will lead to check
        self.from_board_position = None
        self.to_board_position = self.playing_piece
        if self.playing_piece.name == 'King':
            self.king_coords[self.playing_color] = self.to_coords

        # Perform check evaluation
        king_coords = self.king_coords[self.playing_color]
        in_check = True if self._king_in_check(king_coords) else False

        # Return game to previous state
        self.board[self.from_coords.x][self.from_coords.y] = self.playing_piece
        self.board[self.to_coords.x][self.to_coords.y] = original_piece
        self.king_coords[self.playing_color] = original_king_coords

        return in_check

    # def _update_check_status(self):
    #     opponent_king = self._get_king(self.opponent_color)
    #     if _king_in_check(opponent_king.coords):
    #         if self._check_mate(opponent_king):
    #             pass
    #             # TODO Game over


    # def _get_king(self, color):
    #     return [piece for piece in self.board if piece
    #             and piece.color == color and piece.name == 'King'][0]

    def _check_mate(self):
        king_coords = self.king_coords[self.opponent_color]
        # if king_can_move
        if self._can_attack_attacking_piece():
            return False
        if self._piece_can_block_attack(king_coords):
            return False
        return True

    def _can_attack_attacking_piece(self):
        for piece in self._board_pieces(self.playing_color):
            if piece.valid_attack and not self.piece_blocking(piece.coords, self.to_coords):
                return True
        return False

    def _king_in_check(self, coords):
        king_coords = self.king_coords[self.opponent_color]

        for piece in self._board_pieces(self.opponent_color):
            if piece.valid_attack(coords) and not self.piece_blocking(piece.coords, king_coords):
                return True
        return False

    def _piece_can_block_attack(self, king_coords):
        pieces = self._board_pieces(self.playing_color, king=False)
        for coords in self.coords_between(self.to_coords, king_coords):
            for piece in pieces:
                if piece.valid_move(self.to_coords) and not self.piece_blocking(piece.coords, coords):
                    return True
        return False

    def _board_pieces(self, color, king=True):
        if king:
            return [piece for piece in self.board if piece and piece.color == color]
        return [piece for piece in self.board if piece
                and piece.color == color and piece.name != 'King']



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
