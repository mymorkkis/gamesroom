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
        game.display_board()
        try:
            _make_move(game)
        except IllegalMoveError as error:
            _clear_screen()
            print(f'\n{RED}{error.message}{END}\n')

    game.display_board()
    print(f'\n{RED}{game.winner} wins!!! Thanks for playing.....{END}\n')


def _make_move(game):
    """Fetch move input from player, move piece in game.

       Raises:
            IllegalMoveError
    """
    move = input(f'{game.playing_color.value} to move. Choose wisely.....\n --> ')
    try:
        input_from_coords, input_to_coords = move.split()
        from_coords = _coords_from(input_from_coords)
        to_coords = _coords_from(input_to_coords)
        _clear_screen()
        game.move(from_coords, to_coords)
    except (ValueError, KeyError):
        raise IllegalMoveError('Invalid coords, coords seperated by white space. Example usage: a1 a2')


def _coords_from(input_coords):
    input_x, input_y = input_coords
    x_coords = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    y_coords = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}
    x_coord, y_coord = x_coords[input_x], y_coords[input_y]
    return Coords(x_coord, y_coord)


def _clear_screen():
    print('\n' * 50)


if __name__ == '__main__':
    _clear_screen()
    try:
        play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(f'\n{RED}Got too much for you, did it?!?{END}\n')
