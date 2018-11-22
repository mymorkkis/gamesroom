"""Command line script to play chess game."""
import sys

from src.chess_game import ChessGame
from src.othello_game import OthelloGame
from src.game_errors import IllegalMoveError


RED = '\033[91m'
END = '\033[0m'

INVALID_ARG_ERROR = f'''{RED}
Invalid Args provided.....\n
Usage: python play_chess.py GAME_TYPE\n
Game type options: (C)hess, (O)thello
{END}'''

def play():
    """Main function to play chess game."""
    game, make_move = _fetch_game_type()
    _clear_screen()

    while not game.winner:
        game.display_board_to_terminal()
        try:
            make_move(game)
        except IllegalMoveError as error:
            _clear_screen()
            print(f'\n{RED}{error.message}{END}\n')

    game.display_board_to_terminal()
    print(f'\n{RED}{game.winner} wins!!! Thanks for playing.....{END}\n')


def _fetch_game_type():
    try:
        game_type = sys.argv[1].title()[0]
        return GAME[game_type]
    except (KeyError, IndexError):
        print(INVALID_ARG_ERROR)
        exit(1)


def _move_piece(game, single_):
    """Fetch move input from player, move piece in game.

       Raises:
            IllegalMoveError
    """
    move = input(f'{game.playing_color.value} to move. Choose wisely.....\n --> ')
    try:
        from_coords, to_coords = move.split()
        game.process_input_coords([from_coords, to_coords])
        _clear_screen()
    except (ValueError, KeyError):
        raise IllegalMoveError('Invalid coords, coords seperated by white space. Example usage: a1 a2')


def _place_piece(game):
    place_coords = input(f'{game.playing_color.value} to move. Choose wisely.....\n --> ')
    try:
        game.process_input_coords([place_coords])
        _clear_screen()
    except (ValueError, KeyError):
        raise IllegalMoveError('Invalid coords. Example usage: a1')



def _clear_screen():
    print('\n' * 50)


GAME = {
    'C': (ChessGame(), _move_piece),
    'O': (OthelloGame(), _place_piece)
}


if __name__ == '__main__':
    try:
        play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(f'\n{RED}Got too much for you, did it?!?{END}\n')
