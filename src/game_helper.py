"""Module of helper functions for chess game.

   Functions:
        move_direction: Return str representation of move direction.
"""
def move_direction(piece, to_coords):
    """Calculate direction from piece to coordinates. Return str.
       
       Return values: 'diagonal', 'horizontal', 'vertical', 'non_linear'
    """
    if _diagonal_movement(piece, to_coords):
        direction = 'diagonal'
    elif piece.x_coord != to_coords.x and piece.y_coord == to_coords.y:
        direction = 'horizontal'
    elif piece.y_coord != to_coords.y and piece.x_coord == to_coords.x:
        direction = 'vertical'
    else:
        direction = 'non_linear'
    return direction


def _diagonal_movement(piece, coords):
    """Helper function for move_direction. Return bool."""
    min_x_coord, max_x_coord = sorted([piece.x_coord, coords.x])
    min_y_coord, max_y_coord = sorted([piece.y_coord, coords.y])
    # Only diagonal if distance equal lengths
    return (max_x_coord - min_x_coord) == (max_y_coord - min_y_coord)
