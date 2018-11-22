from src.game import Coords
from src.game_enums import Color
from src.othello_game import Othello

def test_othello_board_setup():
    game = Othello()
    expected_board_setup = set([(Color.WHITE, Coords(x=3, y=4)),
                                (Color.WHITE, Coords(x=4, y=3)),
                                (Color.BLACK, Coords(x=3, y=3)),
                                (Color.BLACK, Coords(x=4, y=4))])
    actual_board_setup = set(
        (piece.color, piece.coords)
        for row in game.board
        for piece in row if piece
    )
    assert actual_board_setup == expected_board_setup
