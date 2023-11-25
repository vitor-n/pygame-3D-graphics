import pygame
from pygame.locals import *
import numpy as np
from math import tan, radians, degrees, cos, sin, sqrt
from transforms import *
import time
from input_handler import mouse_handler, keyboard_handler
from camera import Camera
from object_3d import Object_3D
from axes_indicator import AxesIndicator

width = 800
height = 600

fov = radians(90)

scaling_factor = 1/(tan(fov/2))

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

camera = Camera()
camera_axes = AxesIndicator(camera.get_axes(),(50, 50), 20)

grid = Object_3D("meshes/grid.obj", (0, -15, 100), (5,5,5))
airplane = Object_3D("meshes/cessna.obj", (0, 0, 100))
object_axes = AxesIndicator(airplane.get_axes(), (100, 50), 20)

t = 0
fov = 100
zfar = 1000
znear = 0.01

while True:

    t += 10

    rot_world = rotation_z(0) @ rotation_y(0) @ rotation_x(0)
    world_matrix = translation(0,0,0) @ rot_world

    camera.update()

    final_matrix = perspective(fov,height/width,znear,zfar) @ viewport(width,height) @ camera.matrix @ world_matrix

    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            quit()
        if event.type == pygame.MOUSEWHEEL:
            camera.pos_z += 10 * event.y

    # Getting mouse position and rotation angles
    camera.angle_x, camera.angle_y = mouse_handler(width, height, camera.angle_x, camera.angle_y)

    # Handling keyboard inputs
    keyboard_handler(camera, airplane)
    
    screen.fill("black")
    
    grid.update(final_matrix)
    grid.draw_vertex(screen, width, height)
    grid.draw_edges(screen, width, height, "#222222")

    airplane.update(final_matrix)
    airplane.draw_vertex(screen, width, height)

    camera_axes.update(camera.get_axes())
    camera_axes.draw(screen)

    object_axes.update(airplane.get_axes())
    object_axes.draw(screen)

    pygame.draw.circle(screen, "#ff3333", (width//2, height//2), 5, 2)

    pygame.display.update()
    clock.tick(60)