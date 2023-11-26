import pygame
import asyncio
from pygame.locals import *
from transforms import *
from math import tan, radians, pi
from input_handler import mouse_handler, keyboard_handler
from camera import Camera
from object_3d import Object_3D, Axes
from axes_indicator import AxesIndicator

width = 800
height = 600

fov = radians(90)

scaling_factor = 1/(tan(fov/2))

pygame.init()
my_font = pygame.font.SysFont("Comic Sans MS", 30)

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

camera = Camera()

axes = Axes("meshes/axes.obj")
grid = Object_3D("meshes/grid.obj")
cube = Object_3D("meshes/cube.obj")
airplane = Object_3D("meshes/cessna.obj")
camera_axes = AxesIndicator(camera.get_axes(),(50, 60), 20)
object_axes = AxesIndicator(cube.get_axes(), (110, 50), 20)

fov = 100
zfar = 1000
znear = 0.01

async def main():

    t = 0

    while True:
        t += 0.003

        camera.update()
        view_matrix = viewport(width,height) @ perspective(fov,height/width,znear,zfar) @ camera.matrix 

        grid1_matrix = view_matrix @ translation(0,-15,50) @ rotation_z(0) @ rotation_y(0) @ rotation_x(0) @ scale(5,5,5)
        airpl_matrix = view_matrix @ translation(-40*cos(10*t),80,40+50*sin(10*t)) @ rotation_z(cos(10*t)/10) @ rotation_y(-10*t-pi/2) @ rotation_x(sin(10*t))
        cube1_matrix = view_matrix @ translation(0,0,80) @ rotation_z(0) @ rotation_y(0) @ rotation_x(0) @ scale(sin(t),cos(t),sin(t))
        cube2_matrix = view_matrix @ translation(-30,0,50) @ rotation_z(t) @ rotation_y(t) @ rotation_x(t) @ scale(0.5,0.5,0.5)
        cube3_matrix = view_matrix @ translation(30 + 5*sin(10*t),5*cos(10*t),50+5*sin(10*t)) @ rotation_z(0) @ rotation_y(0) @ rotation_x(0) @ scale(0.5,0.5,0.5)

        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:
                quit()

        # Getting mouse position and rotation angles
        camera.angle_x, camera.angle_y = mouse_handler(width, height, camera.angle_x, camera.angle_y)

        # Handling keyboard inputs
        keyboard_handler(camera, camera)
        
        screen.fill("black")

        camera_text = my_font.render(f"x: {-round(camera.pos_x)} y: {round(camera.pos_y)} z: {round(camera.pos_z)}", False, "white")
        screen.blit(camera_text, (10,10))
        
        grid.update(grid1_matrix)
        grid.draw_vertex(screen, width, height)
        grid.draw_edges(screen, width, height, "#222222")

        #draw the axes display

        axes.update(grid1_matrix)
        axes.draw_edges(screen, width, height)

        axes.update(cube1_matrix @ scale(15,15,15))
        axes.draw_edges(screen, width, height)

        axes.update(cube2_matrix @ scale(15,15,15))
        axes.draw_edges(screen, width, height)

        axes.update(cube3_matrix @ scale(15,15,15))
        axes.draw_edges(screen, width, height)

        axes.update(airpl_matrix @ scale(20,20,20))
        axes.draw_edges(screen, width, height)

        #draw the scene objects

        cube.update(cube1_matrix)
        cube.draw_vertex(screen, width, height)
        cube.draw_edges(screen, width, height)

        cube.update(cube2_matrix)
        cube.draw_vertex(screen, width, height)
        cube.draw_edges(screen, width, height)

        cube.update(cube3_matrix)
        cube.draw_vertex(screen, width, height)
        cube.draw_edges(screen, width, height)

        airplane.update(airpl_matrix)
        airplane.draw_vertex(screen, width, height)

        camera_axes.update(camera.get_axes())
        camera_axes.draw(screen)

        #object_axes.update(cube.get_axes())
        #object_axes.draw(screen)

        pygame.draw.circle(screen, "#ff3333", (width//2, height//2), 5, 2)

        pygame.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())