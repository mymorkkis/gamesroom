"""1st attempt at tkinter chess board"""
import tkinter as tk
from tkinter import messagebox

from src.chess_game import ChessGame
from src.game_errors import IllegalMoveError


class Board(tk.Frame):
    """Main tkinter frame"""
    def __init__(self, parent, game, size=64, square_color1="white", square_color2="grey"):
        self.game = game
        self.size = size
        self.square_color1 = square_color1
        self.square_color2 = square_color2
        # self.pieces = {}

        canvas_width = (self.game.board_height + 2) * size
        canvas_height = (self.game.board_width + 2) * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(
            self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height, background="bisque"
        )
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # Will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.refresh)

        self.statusbar = tk.Frame(self)
        self._setup_statusbar()
        self.statusbar.pack(expand=False, fill="x", side='bottom')


    def _setup_statusbar(self):
        tk.Button(self.statusbar, text="Resign", command=None).pack(side="left", padx=10)

        tk.Button(self.statusbar, text="Save", command=None).pack(side="left", padx=10)

        tk.Button(self.statusbar, text='Next move...', command=self.make_move).pack(side="right", padx=10)

        self.move_entry = tk.Entry(self.statusbar, width=10)
        self.move_entry.pack(side="right", padx=10)

    def make_move(self):
        try:
            input_from_coords, input_to_coords = self.move_entry.get().split()
            self.game.process_coords(input_from_coords, input_to_coords)
            self.refresh(event=None)
        except (ValueError, KeyError):
            error_message = 'Invalid coords, coords seperated by white space. Example usage: a1 a2'
            messagebox.showerror("Incorrect coords entered!", error_message)
        except IllegalMoveError as error:
            messagebox.showerror("Illegal move!", error.message)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        # self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    def refresh(self, event):
        """Redraw the board, either move taken or window being resized"""
        if event:
            self._readjust_board_size(event)

        # test_board = self.game.gui_display_board()

        self.canvas.delete('piece')
        self.canvas.delete("square")
        square_color = self.square_color2

        for y_idx, row in enumerate(self.game.gui_display_board()):
            square_color = self._next_square_color(square_color)
            for x_idx, piece in enumerate(row):
                # Plot points for square corners
                x1, y1 = (x_idx * self.size), (y_idx * self.size)
                x2, y2 = x1 + self.size, y1 + self.size

                if ((y_idx == 0 or y_idx == len(self.game.gui_display_board()) - 1)
                        and (x_idx != 0 or x_idx != len(row) -1)):
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, outline="black", fill="brown", tags="border_square"
                    )
                    axis_square = self.canvas.create_text(
                        y_idx, x_idx, text=str(piece), font=("Courier", y1 - y2), tags='x_axis', anchor='c'
                    )
                    self.placepiece(axis_square, y_idx, x_idx)
                elif x_idx == 0 or x_idx == len(row) -1:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, outline="black", fill="brown", tags="border_square"
                    )
                    axis_square = self.canvas.create_text(
                        y_idx, x_idx, text=str(piece), font=("Courier", y1 - y2), tags='y_axis', anchor='c'
                    )
                    self.placepiece(axis_square, y_idx, x_idx)
                else:
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, outline="black", fill=square_color, tags="square"
                    )

                    if piece:
                        piece = self.canvas.create_text(
                            y_idx, x_idx, text=str(piece), font=("Courier", y1 - y2), tags='piece', anchor='c'
                        )
                        self.placepiece(piece, y_idx, x_idx)

                    square_color = self._next_square_color(square_color)

        # for name in self.pieces:
        #     self.placepiece(name, self.pieces[name][0], self.pieces[name][1])

        # self.canvas.tag_raise("piece")
        # self.canvas.tag_lower("square")

    def _readjust_board_size(self, event):
        xsize = int((event.width-1) / (self.game.board_height + 2))
        ysize = int((event.height-1) / (self.game.board_width + 2))
        self.size = min(xsize, ysize)

    def _next_square_color(self, current_color):
        return self.square_color1 if current_color == self.square_color2 else self.square_color2


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Max's Chess")
    chess_game = ChessGame()
    board = Board(root, chess_game)
    board.pack(side=tk.TOP, fill="both", expand="true", padx=4, pady=4)
    root.mainloop()
