import pygame
import numpy as np
from typing import Tuple
from transforms import *
class Object_3D:
    def __init__(self, file_path: str, initial_pos: Tuple[int] = (0, 0, 0), scaling_factors: Tuple[float] = (1,1,1)):

        self.initial_pos = initial_pos
        file = open(file_path)
        self.vertices = []
        self.faces = []
        self.relative_vertices = []
        for line in file:
            if line.startswith("v"):
                try:
                    _, x,y,z = line.split()
                except:
                    pass

                x = float(x)
                y = float(y) 
                z = float(z)

                self.vertices.append([x,y,z,1])

            if line.startswith("f"):
                _, *indices = line.split()
                indices = [int(x) for x in indices]
                self.faces.append(indices)
        
        self.vertices @= scale(*scaling_factors)

        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0

    def update(self, view_matrix: np.ndarray):
        self.relative_vertices = self.vertices @ (view_matrix @ translation(*self.initial_pos)).transpose()

    def draw_vertex(self, screen: pygame.Surface, width: int, height: int):
        for vertex in self.relative_vertices:
            if vertex[0,3] < 0:
                pygame.draw.circle(screen, "white", (vertex[0,0] / vertex[0,3] + width//2, vertex[0,1]/vertex[0,3] + height//2), 1)

    def draw_edges(self, screen: pygame.Surface, width: int, height: int, color = "white"):
        for face in self.faces:
            face_len = len(face)
            for i in range(face_len):
                index_1 = face[i] - 1
                index_2 = face[(i + 1) % face_len] - 1 

                w1 = self.relative_vertices[index_1,3]
                w2 = self.relative_vertices[index_2,3]

                if w1 < 0 and w2 < 0:

                    point_1a = self.relative_vertices[index_1,0] / w1
                    point_1b = self.relative_vertices[index_1,1] / w1

                    point_2a = self.relative_vertices[index_2,0] / w2
                    point_2b = self.relative_vertices[index_2,1] / w2

                    pygame.draw.line(screen, color, (point_1a + 400, point_1b + 300), (point_2a + 400, point_2b + 300), 1)

    def get_axes(self):
        lookat_vector = (rotation_y(self.angle_y) @ rotation_x(self.angle_x) @ (0,0,1,0))[0,:3]
        
        n_vector = lookat_vector
        u_vector = np.cross([0,1,0], n_vector)
        v_vector = np.cross(n_vector, u_vector)

        n_vector = n_vector / np.linalg.norm(n_vector)
        u_vector = u_vector / np.linalg.norm(u_vector)
        v_vector = v_vector / np.linalg.norm(v_vector)

        return u_vector, v_vector, n_vector

    @property
    def angle_x(self):
        return self._angle_x
    
    @angle_x.setter
    def angle_x(self, new_angle_x):
        self.vertices = self.vertices @ rotation_x(new_angle_x - self._angle_x)
        self._angle_x = new_angle_x

    @property
    def angle_y(self):
        return self._angle_y
    
    @angle_y.setter
    def angle_y(self, new_angle_y):
        self.vertices = self.vertices @ rotation_y(new_angle_y - self._angle_y)
        self._angle_y = new_angle_y

    @property
    def angle_z(self):
        return self._angle_z
    
    @angle_z.setter
    def angle_z(self, new_angle_z):
        self.vertices = self.vertices @ rotation_z(new_angle_z - self._angle_z)
        self._angle_z = new_angle_z