import pygame
from math import tan, radians, degrees, cos, sin, sqrt
import numpy as np

def mouse_handler(screen_width, screen_height, angle_x, angle_y):
    """
    Gets screen width, height and the angles the viewer is facing.
    Uses the mouse position to get the angle the view should be rotated
    Then, snaps the mouse position to the center of the window.

    Returns the angle_x and angle_y
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_vector = np.array((screen_width//2 - mouse_x, screen_height//2 - mouse_y)) / 10
    angle_y -= radians(mouse_vector[0])
    angle_x -= radians(mouse_vector[1])
    pygame.mouse.set_pos((screen_width//2, screen_height//2))

    return angle_x, angle_y