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
        (disc.color, disc.coords)
        for row in game.board
        for disc in row if disc
    )
    assert actual_board_setup == expected_board_setup


def test_can_place_piece_and_trap_an_opponent_disc():
    game = Othello()

    assert game.board[5][3] is None
    assert game.board[4][3].color == Color.WHITE

    game.move(Coords(x=5, y=3))
    assert game.board[5][3].color == Color.BLACK
    assert game.board[4][3].color == Color.BLACK
