'''Project enums

   Color: WHITE
          BLACK

   Movement: HORIZONTAL
             DIAGONAL
             VERTICAL
             NON_LINEAR

'''
from enum import Enum, auto

class Color(Enum):
    WHITE = auto()
    BLACK = auto()


class Movement(Enum):
    HORIZONTAL = auto()
    DIAGONAL = auto()
    VERTICATL = auto()
    NON_LINEAR = auto()
