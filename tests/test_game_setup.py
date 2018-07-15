"""Test module for game_setup."""
import pytest

from src.game_enums import Color
from src.game_setup import new_chess_setup

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
