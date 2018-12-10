import pytest

from src.game_enums import Color
from src.game import Coords
from src.draughts_game import DraughtsGame
from src.game_pieces.draughts_counter import Counter
from src.game_errors import IllegalMoveError


def test_draughts_setup_correctly():
    game = DraughtsGame()
    expected_board_setup = set([
        (Color.WHITE, Coords(x=0, y=0)),
        (Color.WHITE, Coords(x=2, y=0)),
        (Color.WHITE, Coords(x=4, y=0)),
        (Color.WHITE, Coords(x=6, y=0)),
        (Color.WHITE, Coords(x=1, y=1)),
        (Color.WHITE, Coords(x=3, y=1)),
        (Color.WHITE, Coords(x=5, y=1)),
        (Color.WHITE, Coords(x=7, y=1)),
        (Color.WHITE, Coords(x=0, y=2)),
        (Color.WHITE, Coords(x=2, y=2)),
        (Color.WHITE, Coords(x=4, y=2)),
        (Color.WHITE, Coords(x=6, y=2)),
        (Color.BLACK, Coords(x=1, y=5)),
        (Color.BLACK, Coords(x=3, y=5)),
        (Color.BLACK, Coords(x=5, y=5)),
        (Color.BLACK, Coords(x=7, y=5)),
        (Color.BLACK, Coords(x=0, y=6)),
        (Color.BLACK, Coords(x=2, y=6)),
        (Color.BLACK, Coords(x=4, y=6)),
        (Color.BLACK, Coords(x=6, y=6)),
        (Color.BLACK, Coords(x=1, y=7)),
        (Color.BLACK, Coords(x=3, y=7)),
        (Color.BLACK, Coords(x=5, y=7)),
        (Color.BLACK, Coords(x=7, y=7))
    ])
    actual_board_setup = set(
        (counter.color, counter.coords)
        for row in game.board
        for counter in row if counter
    )
    assert actual_board_setup == expected_board_setup


def test_draughts_piece_can_move():
    game = DraughtsGame()
    game.playing_color = Color.WHITE
    assert game.board[5][3] is None

    game.move(Coords(x='e', y='3'), Coords(x='f', y='4'))
    assert game.board[4][2] is None
    assert game.board[5][3] == Counter(Color.WHITE)


def test_illegal_move_raises_exception():
    game = DraughtsGame()
    game.playing_color = Color.WHITE

    with pytest.raises(IllegalMoveError, match=game.ILLEGAL_MOVE):
        game.move(Coords(x='e', y='3'), Coords(x='e', y='4'))


def test_same_from_and_to_coords_raises_exception():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
    })

    with pytest.raises(IllegalMoveError, match=game.SAME_SQUARE):
        game.move(Coords(x='g', y='7'), Coords(x='g', y='7'))


def test_no_counter_at_from_coords_raises_exception():
    game = DraughtsGame({})  # empty board

    with pytest.raises(IllegalMoveError, match=game.NO_PIECE):
        game.move(Coords(x='g', y='7'), Coords(x='f', y='6'))


def test_draughts_piece_can_capture():
    game = DraughtsGame({
        '00': Counter(Color.WHITE),
        '11': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE

    game.move(Coords(x='a', y='1'), Coords(x='c', y='3'))
    assert game.board[1][1] is None
    assert game.board[2][2] == Counter(Color.WHITE)


def test_illegal_capture_raises_exception():
    game = DraughtsGame({
        '00': Counter(Color.WHITE),
    })
    game.playing_color = Color.WHITE

    with pytest.raises(IllegalMoveError, match=game.ILLEGAL_CAPTURE):
        game.move(Coords(x='a', y='1'), Coords(x='c', y='3'))


def test_counters_can_be_crowned():
    game = DraughtsGame({
        '16': Counter(Color.WHITE),
        '11': Counter(Color.BLACK),
    })
    black_piece = game.board[1][1]
    white_piece = game.board[1][6]

    assert str(black_piece) == '\u26C2'
    assert not black_piece.crowned

    game.move(Coords(x='b', y='2'), Coords(x='a', y='1'))
    assert black_piece.crowned
    assert str(black_piece) == '\u26C3'

    assert str(white_piece) == '\u26C0'
    assert not white_piece.crowned

    game.move(Coords(x='b', y='7'), Coords(x='a', y='8'))
    assert white_piece.crowned
    assert str(white_piece) == '\u26C1'


def test_crowned_white_piece_can_capture_backwards():
    game = DraughtsGame({
        '22': Counter(Color.WHITE),
        '11': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE
    game.board[2][2].crowned = True

    game.move(Coords(x='c', y='3'), Coords(x='a', y='1'))
    assert game.board[1][1] is None
    assert game.board[0][0] == Counter(Color.WHITE)


def test_crowned_black_piece_can_capture_backwards():
    game = DraughtsGame({
        '55': Counter(Color.BLACK),
        '66': Counter(Color.WHITE),
    })
    game.board[5][5].crowned = True

    game.move(Coords(x='f', y='6'), Coords(x='h', y='8'))
    assert game.board[6][6] is None
    assert game.board[7][7] == Counter(Color.BLACK)


def test_can_capture_two_pieces_in_straight_line():
    game = DraughtsGame({
        '00': Counter(Color.WHITE),
        '11': Counter(Color.BLACK),
        '33': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE

    game.move(Coords(x='a', y='1'), Coords(x='e', y='5'))
    assert game.board[1][1] is None
    assert game.board[3][3] is None
    assert game.board[4][4] == Counter(Color.WHITE)


def test_can_capture_two_pieces_in_multiple_direction():
    game = DraughtsGame({
        '00': Counter(Color.WHITE),
        '11': Counter(Color.BLACK),
        '13': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE

    game.move(Coords(x='a', y='1'), Coords(x='a', y='5'))
    assert game.board[1][1] is None
    assert game.board[1][3] is None
    assert game.board[0][4] == Counter(Color.WHITE)


def test_black_can_capture_two_pieces_in_multiple_direction():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '53': Counter(Color.WHITE),
    })

    game.move(Coords(x='g', y='7'), Coords(x='g', y='3'))
    assert game.board[5][5] is None
    assert game.board[5][3] is None
    assert game.board[6][2] == Counter(Color.BLACK)


def test_can_capture_three_pieces_in_straight_line():
    game = DraughtsGame({
        '77': Counter(Color.BLACK),
        '66': Counter(Color.WHITE),
        '44': Counter(Color.WHITE),
        '22': Counter(Color.WHITE),
    })

    game.move(Coords(x='h', y='8'), Coords(x='b', y='2'))
    assert game.board[6][6] is None
    assert game.board[4][4] is None
    assert game.board[2][2] is None
    assert game.board[1][1] == Counter(Color.BLACK)

def test_white_can_capture_three_pieces_in_multiple_directions_l_shape():
    game = DraughtsGame({
        '60': Counter(Color.WHITE),
        '51': Counter(Color.BLACK),
        '33': Counter(Color.BLACK),
        '35': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE

    game.move(Coords(x='g', y='1'), Coords(x='e', y='7'))
    assert game.board[5][1] is None
    assert game.board[3][3] is None
    assert game.board[3][5] is None
    assert game.board[4][6] == Counter(Color.WHITE)


def test_white_can_capture_three_pieces_in_multiple_directions_s_shape():
    game = DraughtsGame({
        '60': Counter(Color.WHITE),
        '51': Counter(Color.BLACK),
        '53': Counter(Color.BLACK),
        '55': Counter(Color.BLACK),
    })
    game.playing_color = Color.WHITE

    game.move(Coords(x='g', y='1'), Coords(x='e', y='7'))
    assert game.board[5][1] is None
    assert game.board[5][3] is None
    assert game.board[5][5] is None
    assert game.board[4][6] == Counter(Color.WHITE)


def test_black_can_capture_three_pieces_in_multiple_directions_s_shape():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '53': Counter(Color.WHITE),
        '51': Counter(Color.WHITE),
    })

    game.move(Coords(x='g', y='7'), Coords(x='e', y='1'))
    assert game.board[5][5] is None
    assert game.board[5][3] is None
    assert game.board[5][1] is None
    assert game.board[4][0] == Counter(Color.BLACK)


def test_move_raises_error_if_capture_possible_for_piece():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
    })

    with pytest.raises(IllegalMoveError, match=game.CAPTURE_POSSIBLE):
        game.move(Coords(x='g', y='7'), Coords(x='h', y='6'))


def test_move_raises_error_if_capture_possible_for_crowned_piece():
    game = DraughtsGame({
        '77': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '64': Counter(Color.BLACK)
    })
    game.board[6][4].crowned = True

    with pytest.raises(IllegalMoveError, match=game.CAPTURE_POSSIBLE):
        game.move(Coords(x='h', y='8'), Coords(x='g', y='7'))


def test_one_piece_capture_forced_to_make_two_move_capture_if_possible():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '33': Counter(Color.WHITE),
    })

    game.move(Coords(x='g', y='7'), Coords(x='e', y='5'))
    assert game.board[6][6] is None
    assert game.board[5][5] is None
    assert game.board[4][4] is None
    assert game.board[3][3] is None
    assert game.board[2][2] == Counter(Color.BLACK)


def test_two_piece_capture_force_to_make_three_move_capture_if_possible():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '33': Counter(Color.WHITE),
        '11': Counter(Color.WHITE),
    })

    game.move(Coords(x='g', y='7'), Coords(x='c', y='3'))
    assert game.board[6][6] is None
    assert game.board[5][5] is None
    assert game.board[3][3] is None
    assert game.board[2][2] is None
    assert game.board[1][1] is None
    assert game.board[0][0] == Counter(Color.BLACK)


def test_two_extra_captures_forced_if_possible():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '33': Counter(Color.WHITE),
        '11': Counter(Color.WHITE),
    })

    game.move(Coords(x='g', y='7'), Coords(x='e', y='5'))
    assert game.board[6][6] is None
    assert game.board[5][5] is None
    assert game.board[3][3] is None
    assert game.board[1][1] is None
    assert game.board[0][0] == Counter(Color.BLACK)


def test_crowned_piece_can_take_two_pieces_and_return_to_same_y_index():
    game = DraughtsGame({
        '66': Counter(Color.BLACK),
        '55': Counter(Color.WHITE),
        '35': Counter(Color.WHITE),
    })
    game.board[6][6].crowned = True

    game.move(Coords(x='g', y='7'), Coords(x='c', y='7'))
    assert game.board[5][5] is None
    assert game.board[3][5] is None
    assert game.board[2][6] == Counter(Color.BLACK)
