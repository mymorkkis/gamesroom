from flask import Flask, jsonify, request, render_template, session, url_for
from flask_session import Session

from src.games.chess import Chess
from src.game_errors import IllegalMoveError


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    Session(app)

    @app.route('/')
    def home():
        session['current_game'] = None
        return 'Home'

    @app.route('/chess')
    def chess():
        game = Chess()
        square_colors = ('light', 'dark')
        session['current_game'] = game

        return render_template('game.html', board=game.display_board(),
                               x_axis=game.x_axis(), square_colors=square_colors)

    @app.route('/move')
    def move():
        from_coords = request.args.get('from')
        to_coords = request.args['to']
        game = session['current_game']

        try:
            from_piece, to_piece = game.move(from_coords, to_coords)

            return jsonify(from_image=str(from_piece) if from_piece else '',
                           to_image=str(to_piece) if to_piece else '', err='')

        except IllegalMoveError as err:
            return jsonify(err=err.message)

    return app
