from src.game_pieces.game_piece import GamePiece

class Disc(GamePiece):
    def __init__(self, color):
        super().__init__()
        self.color = color

    def __str__(self):
        return str(self.color)

    def legal_move(self, to_coords):
        pass

    def legal_capture(self, to_coords):
        pass
