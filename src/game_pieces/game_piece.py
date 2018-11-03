"""Module for GamePiece abstract base class."""
from abc import ABC, abstractmethod

from src.game_enums import Color


class GamePiece(ABC):
    """Abstract Base class for game pieces.

       Attributes:
            name:   Class name as str
            color:  Piece color (Color Enum)
            coords: Piece current coordinates on board

       Abstract methods:
            legal_move:    Logic to decide legal move for piece
            legal_capture: Logic to decide legal capture for piece
    """
    def __init__(self):
        self.name = self.__class__.__name__
        self._color = None
        self.coords = None

    def __repr__(self):
        return f'{self.name}({self.color.value!r})'

    def __str__(self):
        # return f'{self.color.value} {self.name}: {self.coords!r}'
        NotImplementedError

    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return (self.name, self.color) == (other.name, other.color)
        return NotImplemented

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        if color not in Color:
            # AttributeError thrown if illegal Color Enum, TODO Why can't I catch it?
            raise ValueError('Not a legal game color')
        self._color = color

    @abstractmethod
    def legal_move(self, to_coords):
        """Confirm if move at passed coordinates supported by this piece. Return bool."""
        raise NotImplementedError()

    @abstractmethod
    def legal_capture(self, to_coords):
        """Confirm if capture at passed coordinates supported by this piece. Return bool."""
        raise NotImplementedError()
