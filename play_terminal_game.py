"""Command line script to play chess game."""
from src.games.chess import Chess
from src.games.draughts import Draughts
from src.games.othello import Othello
from src.game_errors import IllegalMoveError
from src.command_line_helper import parse_args_to_fetch_game, RED, END


QUIT_MSG = f'\n{RED}Got too much for you, did it?!?{END}\n'
WINNER_MSG = f'\n{RED}%s wins!!! Thanks for playing.....{END}\n'


GAME_OPTIONS = {
    'C': (Chess()),
    'D': (Draughts()),
    'O': (Othello())
}


def play():
    """Main function to play game."""
    game = parse_args_to_fetch_game(GAME_OPTIONS)
    _clear_screen()

    while not game.winner:
        game.display_board_to_terminal()
        try:
            move_coords = _fetch_input_coords(current_player=game.playing_color.value)
            game.move(*move_coords)
            _clear_screen()
        except IllegalMoveError as error:
            _clear_screen()
            print(f'\n{RED}{error.message}{END}\n')

    game.display_board_to_terminal()
    print(WINNER_MSG % game.winner)


def _fetch_input_coords(current_player):
    move_coords = input(f'{current_player} to move. Choose wisely.....\n --> ')
    if len(move_coords) > 2:
        from_coords, to_coords = move_coords.split()
        return from_coords, to_coords
    return move_coords


def _clear_screen():
    print('\n' * 50)


if __name__ == '__main__':
    try:
        play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(QUIT_MSG)
