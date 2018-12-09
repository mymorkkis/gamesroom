"""User defined exceptions for chess game.

   Exceptions:
        NotOnBoardError:    Passed coordinates not on game board
        IllegalMoveError:   Illegal move attempted
"""
class GameError(Exception):
    """Base class for exceptions in this module."""
    pass


class NotOnBoardError(GameError):
    """Exception raised for passed coordinates are not on game board.

       Attributes:
            coords:  Coordinates that caused the exception
            message: Explanation of the error
    """
    def __init__(self, coords, message):
        self.coords = coords
        self.message = message


class IllegalMoveError(GameError):
    """Exception raised when Illegal move attempted on game board.

       Attributes:
            message: Explanation of the error
    """
    def __init__(self, message):
        self.message = message
