"""1st attempt at tkinter chess board"""
from itertools import cycle
from copy import deepcopy

import tkinter as tk
from tkinter import messagebox, simpledialog

from src.chess_game import ChessGame
from src.othello_game import OthelloGame
from src.game_errors import IllegalMoveError
from src.command_line_helper import parse_args_to_fetch_game


BORDER_SIZE = 2
WHITE = 'white'
BLACK = 'black'
RED = 'red'
GREEN = 'green'
LIGHT_BROWN = '#804000'
DARK_BROWN = '#1a0300'
LIGHT_GREY = '#adad85'


class Board(tk.Frame):
    """Main tkinter frame"""
    def __init__(self, parent, game, square_colors, two_coord_move, err_msg, pixel_size=64):
        self.game = game
        self.pixel_size = pixel_size
        self.square_colors = square_colors
        self.illegal_coord_error_message = err_msg
        self.new_chess_setup = deepcopy(game.board)
        self.move = self._two_coord_move if two_coord_move else self._one_coord_move

        canvas_width = (self.game.board_height + BORDER_SIZE) * pixel_size
        canvas_height = (self.game.board_width + BORDER_SIZE) * pixel_size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height,
                                background='bisque')
        self.canvas.pack(side='top', fill='both', expand=True)

        # Will cause a refresh if the user interactively changes the window size
        self.canvas.bind('<Configure>', self.refresh)

        self._setup_statusbar()

    def _setup_statusbar(self):
        statusbar = tk.Frame(self, height=30)
        # TODO
        tk.Button(statusbar, text='Save Game', command=None).pack(side='left', padx=10)
        # TODO
        tk.Button(statusbar, text='Resign', command=None).pack(side='left', padx=10)

        self.move_entry = tk.Entry(statusbar, width=10)
        self.move_entry.pack(side='left', padx=10)
        self.move_entry.focus()
        self.move_entry.bind('<Return>', self.make_move)

        self.label_status = tk.Label(statusbar, text=None, fg=BLACK)
        self.label_status.pack(side='left', expand=0)

        self.play_again_btn = tk.Button(statusbar, text='Play Again?', command=self._play_again)

        statusbar.pack(expand=True, fill='y', side='bottom')


    def make_move(self, event=None):
        try:
            self.move()
            self.move_entry.delete(0, 'end')
            self.refresh()
        except (ValueError, KeyError):
            self.move_entry.delete(0, 'end')
            messagebox.showerror('Incorrect coords entered!', self.illegal_coord_error_message)
            self.refresh()
        except IllegalMoveError as error:
            self.move_entry.delete(0, 'end')
            messagebox.showerror('Illegal move!', error.message)
            self.refresh()

    def _place_item(self, item, row, column):
        """Place a piece at the given row/column"""
        x0 = (column * self.pixel_size) + int(self.pixel_size / 2)
        y0 = (row * self.pixel_size) + int(self.pixel_size / 2)
        self.canvas.coords(item, x0, y0)

    def _one_coord_move(self):
        to_coords = self.move_entry.get()
        self.game.process_input_coords([to_coords])

    def _two_coord_move(self):
        from_coords, to_coords = self.move_entry.get().split()
        self.game.process_input_coords([from_coords, to_coords])

    def refresh(self, event=None):
        """Redraw the board, either move taken or window being resized"""
        if event:
            self._readjust_board_size(event)
        self.canvas.delete('piece', 'square', 'y_axis', 'x_axis', 'border_square')
        self._draw_board_and_pieces()
        self._check_for_winner()

    def _draw_board_and_pieces(self):
        for y_idx, row in enumerate(self.game.gui_display_board()):
            next(self.square_colors)
            for x_idx, piece in enumerate(row):
                idxs = (y_idx, x_idx)
                square_coords, image_size = self._plot_square_coordinates(*idxs)

                if self._x_axis_square(y_idx, x_idx, row):
                    self._create_border_square(
                        square_coords, image_size, piece, idxs, tags='x_axis'
                    )
                elif self._y_axis_square(x_idx, row):
                    self._create_border_square(
                        square_coords, image_size, piece, idxs, tags='y_axis'
                    )
                else:
                    self._create_board_square(
                        square_coords, next(self.square_colors), image_size, piece, idxs
                    )

    def _check_for_winner(self):
        player = self.game.playing_color.name
        if self.game.winner:
            self.move_entry.pack_forget()
            self.label_status['text'] = f'\t{player} wins!!!\t'
            self.label_status['fg'] = RED
            self.play_again_btn.pack(side='left')
        else:
            self.label_status['text'] = f'{player} to move. Enter chess notation e.g. "a1 a2"'

    def _plot_square_coordinates(self, y_idx, x_idx):
        x1, y1 = (x_idx * self.pixel_size), (y_idx * self.pixel_size)
        x2, y2 = x1 + self.pixel_size, y1 + self.pixel_size
        square_coords = x1, y1, x2, y2
        image_size = y1 - y2
        return square_coords, image_size

    def _create_board_square(self, square_coords, square_color, image_size, piece, idxs):
        self.canvas.create_rectangle(
            *square_coords, outline=BLACK, fill=square_color, tags='square'
        )

        if piece:
            piece = self.canvas.create_text(
                *idxs, text=str(piece), font=('Courier', image_size), tags='piece', anchor='c'
            )
            self._place_item(piece, *idxs)

    def _create_border_square(self, square_coords, image_size, piece, idxs, tags):
        axis_char_size = int(image_size / 2)

        self.canvas.create_rectangle(
            *square_coords, outline=DARK_BROWN, fill=DARK_BROWN, tags='border_square'
        )
        axis_square = self.canvas.create_text(
            *idxs, text=str(piece), font=('Courier', axis_char_size), fill=LIGHT_GREY, tags=tags, anchor='c'
        )
        self._place_item(axis_square, *idxs)

    def _x_axis_square(self, y_idx, x_idx, row):
        return (x_idx not in self.first_and_last_index(row)
                and y_idx in self.first_and_last_index(self.game.gui_display_board()))

    def _y_axis_square(self, x_idx, row):
        return x_idx in self.first_and_last_index(row)

    def _readjust_board_size(self, event):
        xsize = int((event.width - 1) / (self.game.board_height + BORDER_SIZE))
        ysize = int((event.height - 1) / (self.game.board_width + BORDER_SIZE))
        self.pixel_size = min(xsize, ysize)

    def _play_again(self):
        self.game.board = self.new_chess_setup
        self.game.winner = None
        self.play_again_btn.pack_forget()
        self.label_status.pack_forget()
        self.move_entry.pack(side='left', padx=10)
        self.label_status.pack(side='left', expand=0)
        self.label_status['fg'] = BLACK
        self.refresh()

    @staticmethod
    def first_and_last_index(item):
        """Return tuple of item first and last index"""
        return 0, len(item) - 1

GAME_OPTIONS = {
    'C': {
        'game': ChessGame(),
        'title': 'Chess Game',
        'square_colors': cycle([WHITE, LIGHT_BROWN]),
        'two_coord_move': True,
        'err_msg': 'Input coords using chess notation, seperated by white space. Example usage: a1 a2'
    },
    'O': {
        'game': OthelloGame(),
        'title': 'Othello Game',
        'square_colors': cycle([GREEN]),
        'two_coord_move': False,
        'err_msg': 'Input coords using chess notation. Example usage: a1'
    }
}


def _play_game():
    root = tk.Tk()
    # game_type = simpledialog.askstring(
    #     'Choose a game to play...', 'Options: (C)hess, (O)thello'
    # ).title()[0]
    # game = GAME[game_type]
    game = parse_args_to_fetch_game(GAME_OPTIONS)
    root.title(game['title'])
    board = Board(parent=root, game=game['game'], square_colors=game['square_colors'],
                  two_coord_move=game['two_coord_move'], err_msg=game['err_msg'])
    board.pack(side='top', fill='y', expand=True, padx=4, pady=4)
    return root


if __name__ == '__main__':
    game = _play_game()
    game.mainloop()