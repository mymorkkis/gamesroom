from src.game_enums import Color
from src.game import Coords
from src.draughts_game import DraughtsGame


def test_draughts_setup_correctly():
    game = DraughtsGame()
    expected_board_setup = set([
        (Color.WHITE, Coords(x=0, y=0)),
        (Color.WHITE, Coords(x=0, y=2)),
        (Color.WHITE, Coords(x=0, y=4)),
        (Color.WHITE, Coords(x=0, y=6)),
        (Color.WHITE, Coords(x=1, y=1)),
        (Color.WHITE, Coords(x=1, y=3)),
        (Color.WHITE, Coords(x=1, y=5)),
        (Color.WHITE, Coords(x=1, y=7)),
        (Color.WHITE, Coords(x=2, y=0)),
        (Color.WHITE, Coords(x=2, y=2)),
        (Color.WHITE, Coords(x=2, y=4)),
        (Color.WHITE, Coords(x=2, y=6)),
        (Color.BLACK, Coords(x=5, y=1)),
        (Color.BLACK, Coords(x=5, y=3)),
        (Color.BLACK, Coords(x=5, y=5)),
        (Color.BLACK, Coords(x=5, y=7)),
        (Color.BLACK, Coords(x=6, y=0)),
        (Color.BLACK, Coords(x=6, y=2)),
        (Color.BLACK, Coords(x=6, y=4)),
        (Color.BLACK, Coords(x=6, y=6)),
        (Color.BLACK, Coords(x=7, y=1)),
        (Color.BLACK, Coords(x=7, y=3)),
        (Color.BLACK, Coords(x=7, y=5)),
        (Color.BLACK, Coords(x=7, y=7))
    ])
    actual_board_setup = set(
        (counter.color, counter.coords)
        for row in game.board
        for counter in row if counter
    )
    assert actual_board_setup == expected_board_setup
