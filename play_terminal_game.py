"""Command line script to play chess game."""
from src.chess_game import ChessGame
from src.othello_game import OthelloGame
from src.game_errors import IllegalMoveError
from src.command_line_helper import parse_args_to_fetch_game, RED, END


GAME_OPTIONS = {
    'C': (ChessGame(), True, 'Invalid coords, coords seperated by white space. Example usage: a1 a2'),
    'O': (OthelloGame(), False, 'Invalid coords. Example usage: a1')
}


def play():
    """Main function to play game."""
    game, two_coord_move, err_msg = parse_args_to_fetch_game(GAME_OPTIONS)
    _clear_screen()

    while not game.winner:
        game.display_board_to_terminal()
        try:
            _move_piece(game, two_coord_move, err_msg)
        except IllegalMoveError as error:
            _clear_screen()
            print(f'\n{RED}{error.message}{END}\n')

    game.display_board_to_terminal()
    print(f'\n{RED}{game.winner} wins!!! Thanks for playing.....{END}\n')


def _move_piece(game, two_coord_move, coord_error_message):
    """Fetch move to/from input from player, move piece in game.

       Raises:
            IllegalMoveError
    """
    move = input(f'{game.playing_color.value} to move. Choose wisely.....\n --> ')
    try:
        if two_coord_move:
            from_coords, to_coords = move.split()
            game.process_input_coords([from_coords, to_coords])
        else:
            game.process_input_coords([move])
        _clear_screen()
    except (ValueError, KeyError):
        raise IllegalMoveError(coord_error_message)


def _clear_screen():
    print('\n' * 50)


if __name__ == '__main__':
    try:
        play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(f'\n{RED}Got too much for you, did it?!?{END}\n')
