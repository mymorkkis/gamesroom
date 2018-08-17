'''Project enums

   Color: WHITE
          BLACK

   Direction: HORIZONTAL
              DIAGONAL
              VERTICAL
              NON_LINEAR

'''
from enum import Enum, auto


class Color(Enum):
    """Colors: WHITE, BLACK"""
    WHITE = auto()
    BLACK = auto()


class Direction(Enum):
    """Directions: HORIZONTAL, DIAGONAL, VERTICAL, NON_LINEAR"""
    HORIZONTAL = auto()
    DIAGONAL = auto()
    VERTICAL = auto()
    NON_LINEAR = auto()
