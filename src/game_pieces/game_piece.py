"""Module for GamePiece abstract base class."""
from abc import ABC, abstractmethod

from src.game_enums import Color


class GamePiece(ABC):
    """Abstract Base class for game pieces.

       Attributes:
            type:    Class name as str
            color:   Piece color (Color Enum)
            x_coord: Piece current x_coordinate on board
            y_coord: Piece current y_coordinate on board

       Abstract methods:
            valid_move:    Logic to decide valid move for piece
            valid_capture: Logic to decide valid capture for piece
    """
    def __init__(self):
        self.type = self.__class__.__name__
        self._color = None
        self.x_coord = None
        self.y_coord = None

    def __repr__(self):
        return f'{self.type}({self.color!r})'

    def __str__(self):
        return (f'{self.color.name.title()} {self.type}: '
                f'x_coord = {self.x_coord}, y_coord = {self.y_coord}')

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if color not in Color:
            # AttributeError thrown if invalid Color Enum
            raise ValueError('Not a valid game color')
        self._color = color
    

    @abstractmethod
    def valid_move(self, to_coords):
        """Confirm if move at passed coordinates supported by this piece. Return bool."""
        raise NotImplementedError() 

    @abstractmethod
    def valid_capture(self, to_coords):
        """Confirm if capture at passed coordinates supported by this piece. Return bool."""
        raise NotImplementedError() 
