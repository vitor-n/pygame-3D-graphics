import pygame
import numpy as np
from typing import Tuple
class Object_3D:
    def __init__(self, file_path: str, initial_pos: Tuple[int] = (0, 0, 0)):
        file = open(file_path)
        self.vertices = []
        self.faces = []
        for line in file:
            if line.startswith("v"):
                try:
                    _, x,y,z = line.split()
                except:
                    pass
                x = float(x) + initial_pos[0]
                y = float(y) + initial_pos[1]
                z = float(z) + initial_pos[2]

                self.vertices.append([x,y,z,1])
                
            if line.startswith("f"):
                _, *indices = line.split()
                self.faces.append(indices)

    def draw(self, screen: pygame.Surface, width: int, height: int, view_matrix: np.ndarray):
        relative_vertices = self.vertices @ view_matrix.transpose()
        for vertex in relative_vertices:
            if vertex[0,3] < 0:
                pygame.draw.circle(screen, "black", (vertex[0,0] / vertex[0,3] + width//2, vertex[0,1]/vertex[0,3] + height//2), 2)
        
