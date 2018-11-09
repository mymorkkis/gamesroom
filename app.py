"""Main Flask app"""
from flask import Flask, render_template

from src.chess_game import ChessGame


app = Flask(__name__)


@app.route('/')
def home():
    return 'Welcome to the game api......'


@app.route('/chess')
def chess():
    game = ChessGame()
    board = game.display_board()
    y_axis = [8, 7, 6, 5, 4, 3, 2, 1, '']
    return render_template('chess.html', board=zip(y_axis, board))


if __name__ == '__main__':
    app.run(debug=True)
