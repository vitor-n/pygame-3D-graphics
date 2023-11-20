import pygame
from math import tan, radians, degrees, cos, sin, sqrt
import numpy as np
from pygame.locals import *
from camera import Camera

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

def keyboard_handler(camera: Camera):
    """
    Handles the keyboard inputs of the program. 
    Calls the camera methods according to the pressed keys, allowing movement.
    """
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        quit()

    if key[K_w]:
        camera.move_forwards()
    if key[K_s]:
        camera.move_backwards()
    if key[K_a]:
        camera.move_left()
    if key[K_d]:
        camera.move_right()
    if key[K_q]:
        camera.move_upwards()
    if key[K_e]:
        camera.move_downwards()
    
    if key[K_UP]:
        camera.angle_x -= 0.001
    if key[K_DOWN]:
        camera.angle_x += 0.001
    if key[K_LEFT]:
        camera.angle_y -= 0.001
    if key[K_RIGHT]:
        camera.angle_y += 0.001