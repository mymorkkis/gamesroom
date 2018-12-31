"""Command line script to play chess, draughts or othello game."""
import sys

from tabulate import tabulate

from src.games.chess import Chess
from src.games.draughts import Draughts
from src.games.othello import Othello
from src.game_errors import IllegalMoveError


class TerminalGame():

    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    NO_MESSAGE = '\n\n'

    INVALID_ARG_ERROR = f'''{RED}
    Invalid Args provided.....\n
    Usage: python {sys.argv[0]} GAME_TYPE\n
    Game type options: (C)hess, (D)raughts, (O)thello
    {END}'''

    QUIT_MSG = f'\n{RED}Got too much for you, did it?!?{END}\n'

    GAME_OPTIONS = {
        'C': Chess(),
        'D': Draughts(),
        'O': Othello()
    }

    X_COORD_MAP = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    Y_COORD_MAP = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7}

    def __init__(self):
        self.game = self._parse_args_to_fetch_game()
        self.display_message = self.NO_MESSAGE
        self.player = None

    def play(self):
        """Main game loop. Continue until winner declared."""
        while not self.game.winner:
            self.player = self.game.playing_color.value
            self._display_board_to_terminal()
            self._make_move()
        self._display_board_and_winner()

    def _parse_args_to_fetch_game(self):
        try:
            game_type = sys.argv[1].title()[0]
            return self.GAME_OPTIONS[game_type]
        except (KeyError, IndexError):
            print(self.INVALID_ARG_ERROR)
            sys.exit()

    def _display_board_and_winner(self):
        self.display_message = f'\n{self.BLUE}{self.player} wins!!! Thanks for playing.....{self.END}\n'
        self._display_board_to_terminal()

    def _make_move(self):
        try:
            move_coords = input(f'{self.player} to move. Choose wisely.....\n --> ')
            self.display_message = self.NO_MESSAGE
            if len(move_coords) > 2:
                move_coords = self._split_and_map_coords(move_coords)
                self.game.move(*move_coords)
            else:
                place_piece_coords = self._map_coords(move_coords)
                self.game.move(to_coords=place_piece_coords)
        except IllegalMoveError as error:
            self.display_message = f'\n{self.RED}{error.message}{self.END}\n'

    def _split_and_map_coords(self, move_coords):
        try:
            from_coords, to_coords = move_coords.split()
            return self._map_coords(from_coords), self._map_coords(to_coords)
        except ValueError:
            raise IllegalMoveError(self.game.input_error_msg)

    def _map_coords(self, input_coords):
        try:
            input_x, input_y = input_coords
            x_coord = self.X_COORD_MAP[str(input_x).lower()]
            y_coord = self.Y_COORD_MAP[str(input_y)]
            return f'{x_coord}{y_coord}'
        except (ValueError, KeyError):
            raise IllegalMoveError(self.game.input_error_msg)

    def _align_board_for_display(self):
        transposed_board = [list(row) for row in zip(*self.game.board)]
        return list(reversed(transposed_board))

    def _display_board_to_terminal(self):
        self._clear_screen()
        board = self._align_board_for_display()
        board.append(self.game.x_axis())
        print(tabulate(board, tablefmt="fancy_grid", showindex=self.game.y_axis()))
        print(self.display_message)

    def _clear_screen(self):
        print('\n' * 50)


if __name__ == '__main__':
    try:
        game = TerminalGame()
        game.play()
    except (KeyboardInterrupt, EOFError):  # Player wants to quit
        print(game.QUIT_MSG)
