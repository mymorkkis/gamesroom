import sys


RED = '\033[91m'
END = '\033[0m'


INVALID_ARG_ERROR = f'''{RED}
Invalid Args provided.....\n
Usage: python {sys.argv[0]} GAME_TYPE\n
Game type options: (C)hess, (O)thello
{END}'''


def parse_args_to_fetch_game(game_options):
    try:
        game_type = sys.argv[1].title()[0]
        return game_options[game_type]
    except (KeyError, IndexError):
        print(INVALID_ARG_ERROR)
        sys.exit()