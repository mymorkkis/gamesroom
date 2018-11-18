"""1st attempt at tkinter chess board"""
from itertools import cycle
from copy import deepcopy

import tkinter as tk
from tkinter import messagebox

from src.chess_game import ChessGame
from src.game_errors import IllegalMoveError


BORDER_SIZE = 2
WHITE = 'white'
BLACK = 'black'
RED = 'red'
LIGHT_BROWN = '#804000'
DARK_BROWN = '#1a0300'
LIGHT_GREY = '#adad85'


class Board(tk.Frame):
    """Main tkinter frame"""
    def __init__(self, parent, game, square_colors, pixel_size=64):
        # self.parent = parent
        self.game = game
        self.pixel_size = pixel_size
        self.square_colors = square_colors
        self.new_chess_setup = deepcopy(game.board)

        canvas_width = (self.game.board_height + BORDER_SIZE) * pixel_size
        canvas_height = (self.game.board_width + BORDER_SIZE) * pixel_size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height,
                                background='bisque')
        self.canvas.pack(side='top', fill='both', expand=True, padx=2, pady=2)

        # Will cause a refresh if the user interactively changes the window size
        self.canvas.bind('<Configure>', self.refresh)

        self._setup_statusbar()

    def _setup_statusbar(self):
        self.statusbar = tk.Frame(self)
        # TODO
        tk.Button(self.statusbar, text='Save Game', command=None).pack(side='left', padx=10)
        # TODO
        tk.Button(self.statusbar, text='Resign', command=None).pack(side='left', padx=20)

        self.move_entry = tk.Entry(self.statusbar, width=10)
        self.move_entry.pack(side='left', padx=10)
        self.move_entry.focus()
        self.move_entry.bind('<Return>', self.make_move)

        self.label_status = tk.Label(self.statusbar, text=None, fg=BLACK)
        self.label_status.pack(side='left', expand=0)

        self.play_again_btn = tk.Button(self.statusbar, text='Play Again?', command=self.play_again)

        self.statusbar.pack(expand=False, fill='x', side='bottom')


    def make_move(self, event=None):
        try:
            from_coords, to_coords = self.move_entry.get().split()
            self.game.process_input_coords(from_coords, to_coords)
            self.move_entry.delete(0, 'end')
            self.refresh()
        except (ValueError, KeyError):
            self.move_entry.delete(0, 'end')
            error_message = 'Input coords using chess notation, seperated by white space. Example usage: a1 a2'
            messagebox.showerror('Incorrect coords entered!', error_message)
        except IllegalMoveError as error:
            self.move_entry.delete(0, 'end')
            messagebox.showerror('Illegal move!', error.message)

    def place_item(self, item, row, column):
        """Place a piece at the given row/column"""
        x0 = (column * self.pixel_size) + int(self.pixel_size / 2)
        y0 = (row * self.pixel_size) + int(self.pixel_size / 2)
        self.canvas.coords(item, x0, y0)

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
            self.place_item(piece, *idxs)

    def _create_border_square(self, square_coords, image_size, piece, idxs, tags):
        axis_char_size = int(image_size / 2)

        self.canvas.create_rectangle(
            *square_coords, outline=DARK_BROWN, fill=DARK_BROWN, tags='border_square'
        )
        axis_square = self.canvas.create_text(
            *idxs, text=str(piece), font=('Courier', axis_char_size), fill=LIGHT_GREY, tags=tags, anchor='c'
        )
        self.place_item(axis_square, *idxs)

    def _x_axis_square(self, y_idx, x_idx, row):
        return (x_idx not in self.first_and_last_index(row)
                and y_idx in self.first_and_last_index(self.game.gui_display_board()))

    def _y_axis_square(self, x_idx, row):
        return x_idx in self.first_and_last_index(row)

    def _readjust_board_size(self, event):
        xsize = int((event.width - 1) / (self.game.board_height + BORDER_SIZE))
        ysize = int((event.height - 1) / (self.game.board_width + BORDER_SIZE))
        self.pixel_size = min(xsize, ysize)

    def play_again(self):
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


def play_chess_game():
    root = tk.Tk()
    root.title("Max's Chess")
    game = ChessGame()
    board = Board(root, game, cycle([WHITE, LIGHT_BROWN]))
    board.pack(side='top', fill='both', expand='true', padx=4, pady=4)
    return root

if __name__ == '__main__':
    chess_game = play_chess_game()
    chess_game.mainloop()
