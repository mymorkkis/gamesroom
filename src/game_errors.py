"""User defined exceptions for chess game.
   
   Exceptions:
        NotOnBoardError:    Passed coordinates not on game board
        PieceNotFoundError: No piece located at from coordinates
        InvalidMoveError:   Invalid move attempted
"""
class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class NotOnBoardError(Error):
    """Exception raised for passed coordinates are not on game board.

       Attributes:
            coords:  Coordinates that caused the exception
            message: Explanation of the error
    """
    def __init__(self, coords, message):
        self.coords = coords
        self.message = message


class PieceNotFoundError(Error):
    """Exception raised when no piece is located at passed from coordinates.

       Attributes:
            coords:  Coordinates that caused the exception
            message: Explanation of the error
    """
    def __init__(self, coords, message):
        self.coords = coords
        self.message = message


class InvalidMoveError(Error):
    """Exception raised when invalid move attempted on game board.

       Attributes:
            from_coords: Attempted to move piece from
            to_coords:   Attempted to move piece to
            message:     Explanation of the error
    """
    def __init__(self, from_coords, to_coords, message):
        self.from_coords = from_coords
        self.to_coords = to_coords
        self.message = message
