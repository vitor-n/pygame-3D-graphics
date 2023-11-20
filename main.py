import pygame
from pygame.locals import *
import numpy as np
from math import tan, radians, degrees, cos, sin, sqrt
from transforms import *
import time
from input_handler import mouse_handler
from camera import Camera
from object import Object

width = 800
height = 600

file = open("cessna.obj")

obj_verts = []
obj_faces = []

for line in file:
    if line.startswith("v"):
        try:
            _, x,y,z = line.split()
        except:
            pass
        obj_verts.append([float(x),float(y),float(z),1])
    if line.startswith("f"):
        _, *indices = line.split()
        obj_faces.append(indices)

fov = radians(90)

scaling_factor = 1/(tan(fov/2))

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

t = 0

fov = 100

zfar = 1000
znear = 0.01

pygame.mouse.set_visible(0)

camera = Camera()

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

    
    screen.fill("#ff5555")

    cube_p = obj_verts @ final_matrix.transpose()

    for vertex in cube_p:
        if vertex[0,3] < 0:
            pygame.draw.circle(screen, "black", (vertex[0,0] / vertex[0,3] + width//2, vertex[0,1]/vertex[0,3] + height//2), 2)
        
    pygame.draw.circle(screen, "white", (width//2, height//2), 5, 2)

    pygame.display.update()
    clock.tick()