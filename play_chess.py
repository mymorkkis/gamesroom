"""Command line script to play chess game."""
from src.chess_game import ChessGame
from src.game import Coords
from src.game_errors import IllegalMoveError


RED = '\033[91m'
END = '\033[0m'


def play():
    """Main function to play chess game."""
    game = ChessGame()

    while not game.winner:
        game.display_board_to_terminal()
        try:
            _make_move(game)
        except IllegalMoveError as error:
            _clear_screen()
            print(f'\n{RED}{error.message}{END}\n')

    game.display_board_to_terminal()
    print(f'\n{RED}{game.winner} wins!!! Thanks for playing.....{END}\n')


def _make_move(game):
    """Fetch move input from player, move piece in game.

       Raises:
            IllegalMoveError
    """
    move = input(f'{game.playing_color.value} to move. Choose wisely.....\n --> ')
    try:
        from_coords, to_coords = move.split()
        game.process_input_coords(from_coords, to_coords)
        _clear_screen()
    except (ValueError, KeyError):
        raise IllegalMoveError('Invalid coords, coords seperated by white space. Example usage: a1 a2')


def _clear_screen():
    print('\n' * 50)


if __name__ == '__main__':
    _clear_screen()
    try:
        play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(f'\n{RED}Got too much for you, did it?!?{END}\n')
