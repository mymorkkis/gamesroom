"""Create main app."""
import os

from flask import Flask, jsonify, request, render_template, session, url_for
from flask_session import Session

from src.games.chess import Chess
from src.games.draughts import Draughts
from src.games.othello import Othello
from src.game_errors import IllegalMoveError


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SESSION_TYPE'] = os.environ.get('SESSION_TYPE', 'filesystem')
    Session(app)

    @app.route('/')
    def home():
        session['current_game'] = None
        return render_template('base.html')

    def play_game(game, *, move_piece_game=True):
        session['current_game'] = game
        return render_template('game.html', game=game, move_piece_game=move_piece_game)

    @app.route('/chess')
    def chess():
        return play_game(Chess())

    @app.route('/draughts')
    def draughts():
        return play_game(Draughts())

    @app.route('/othello')
    def othello():
        return play_game(Othello(), move_piece_game=False)

    @app.route('/move')
    def move():
        from_coords = request.args['from'] if request.args['from'] != 'null' else None
        to_coords = request.args['to']
        game = session['current_game']

        try:
            game.move(from_coords, to_coords)
            return jsonify(board=game.display_board(), err='')
        except IllegalMoveError as err:
            return jsonify(err=err.message)

    return app


app = create_app()
