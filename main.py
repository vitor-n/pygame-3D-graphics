import pygame
from pygame.locals import *
import numpy as np
from math import tan, radians, degrees, cos, sin, sqrt
from transforms import *
import time

h = 600
w = 800

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
screen = pygame.display.set_mode((w,h))
clock = pygame.time.Clock()

t = 0

pos_y = 0
pos_x = 0
pos_z = 0

angle_x = 0
angle_y = 0
angle_z = 0

fov = 100

zfar = 1000
znear = 0.01

vel = 1

pygame.mouse.set_visible(0)

while True:

    t += 10

    rot_world = rotation_z(0) @ rotation_y(0) @ rotation_x(0)
    world_matrix = translation(0,0,0) @ rot_world

    lookat_vector = (rotation_y(angle_y) @ rotation_x(angle_x) @ (0,0,1,0))[0,:3]

    n = lookat_vector
    n /= np.linalg.norm(n)

    u = np.cross([0,1,0], n)
    u /= np.linalg.norm(u)

    v = np.cross(n, u)
    v /= np.linalg.norm(v)

    #rot_camera = camera_orientation(u,v,n)
    rot_camera = (rotation_y(angle_y) @ rotation_x(angle_x)).transpose()

    camera_matrix = rot_camera @ camera_translation((pos_x, pos_y, pos_z))

    final_matrix = perspective(fov,h/w,znear,zfar) @ viewport(w,h) @ camera_matrix @ world_matrix

    for event in pygame.event.get():
        if event.type in [pygame.QUIT]:
            quit()
        if event.type == pygame.MOUSEWHEEL:
            pos_z += 10 * event.y

    # Getting mouse position and rotation angles
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_vector = np.array((w//2 - mouse_x, h//2 - mouse_y)) / 10
    angle_y -= radians(mouse_vector[0])
    angle_x -= radians(mouse_vector[1])
    pygame.mouse.set_pos((w//2,h//2))

    print("uvn: ", u,v,n)
    #print("pos xyz: ", (pos_x,pos_y,pos_z))
    #print("angles: ", degrees(angle_x), degrees(angle_y))


    # Handling keyboard inputs
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        quit()

    if key[K_w]:
        pos_x += n[0,0] * vel
        #pos_y += n[0,1] * vel
        pos_z += n[0,2] * vel 
    if key[K_s]:
        pos_x -= n[0,0] * vel 
        #pos_y -= n[0,1] * vel
        pos_z -= n[0,2] * vel
    if key[K_a]:
        pos_x += u[0,0] * vel
        #pos_y -= u[0,1] * vel
        pos_z += u[0,2] * vel
    if key[K_d]:
        pos_x -= u[0,0] * vel
        #pos_y += u[0,1] * vel
        pos_z -= u[0,2] * vel
    if key[K_q]:
        pos_y += 1 * vel 
    if key[K_e]:
        pos_y -= 1 * vel
    
    if key[K_UP]:
        angle_x -= 0.001
    if key[K_DOWN]:
        angle_x += 0.001
    if key[K_LEFT]:
        angle_y -= 0.001
    if key[K_RIGHT]:
        angle_y += 0.001

    
    screen.fill("#ff5555")

    cube_p = obj_verts @ final_matrix.transpose()

    for vertex in cube_p:
        if vertex[0,3] < 0:
            pygame.draw.circle(screen, "black", (vertex[0,0] / vertex[0,3] + w//2, vertex[0,1]/vertex[0,3] + h//2), 2)
        
    pygame.draw.circle(screen, "white", (w//2, h//2), 5, 2)

    pygame.display.update()
    clock.tick()