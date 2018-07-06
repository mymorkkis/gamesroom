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
    WHITE = auto()
    BLACK = auto()


class Direction(Enum):
    HORIZONTAL = auto()
    DIAGONAL = auto()
    VERTICAL = auto()
    NON_LINEAR = auto()
