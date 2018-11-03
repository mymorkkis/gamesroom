'''Project enums

   Color: WHITE
          BLACK

   Direction: HORIZONTAL
              DIAGONAL
              VERTICAL
              NON_LINEAR

'''
from enum import auto, Enum, unique


@unique
class Color(Enum):
    """Colors: WHITE, BLACK"""
    WHITE = 'White'
    BLACK = 'Black'


@unique
class ChessPiece(Enum):
    KING = 'King'
    QUEEEN = 'Queen'
    ROOK = 'Rook'
    BISHOP = 'Bishop'
    KNIGHT = 'Knight'
    PAWN = 'Pawn'


class Direction(Enum):
    """Directions: HORIZONTAL, DIAGONAL, VERTICAL, NON_LINEAR"""
    HORIZONTAL = auto()
    DIAGONAL = auto()
    VERTICAL = auto()
    NON_LINEAR = auto()
