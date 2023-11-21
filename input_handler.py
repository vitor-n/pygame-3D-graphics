import pygame
from math import tan, radians, degrees, cos, sin, sqrt
import numpy as np
from pygame.locals import *
from camera import Camera
from object_3d import Object_3D

def mouse_handler(screen_width, screen_height, angle_x, angle_y):
    """
    Gets screen width, height and the angles the viewer is facing.
    Uses the mouse position to get the angle the view should be rotated
    Then, snaps the mouse position to the center of the window.

    Returns the angle_x and angle_y
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x != 0 and mouse_y != 0:
        mouse_vector = np.array((screen_width//2 - mouse_x, screen_height//2 - mouse_y)) / 10
        angle_y -= radians(mouse_vector[0])
        angle_x -= radians(mouse_vector[1])
        pygame.mouse.set_pos((screen_width//2, screen_height//2))

    return angle_x, angle_y

def keyboard_handler(camera: Camera, object: Object_3D):
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
        object.angle_x -= radians(1)
    if key[K_DOWN]:
        object.angle_x += radians(1)
    if key[K_LEFT]:
        object.angle_y -= radians(1)
    if key[K_RIGHT]:
        object.angle_y += radians(1)