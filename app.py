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
    board = zip(game.y_axis, game.display_board())
    return render_template('chess.html', board=board, x_axis=game.x_axis)


if __name__ == '__main__':
    app.run(debug=True)
