from typing import Tuple
import pygame
from transforms import *
import numpy as np

class AxesIndicator:
    def __init__(self, vectors: Tuple, center: Tuple[int], line_size:int) -> None:
        self.vec_x, self.vec_y, self.vec_z = vectors
        self.center = center
        self.line_size = line_size
    
    def update(self, new_vectors: Tuple):
        self.vec_x, self.vec_y, self.vec_z = new_vectors

    def draw(self, screen: pygame.Surface):
        vectors_matrix = np.concatenate((self.vec_x, self.vec_y, self.vec_z))
        projection_matrix = np.array(([1, 0, 0], [0, 1, 0]))
        add_center_matrix = np.array(([self.center[0], self.center[1]], 
                                      [self.center[0], self.center[1]], 
                                      [self.center[0], self.center[1]]))

        projected_matrix = projection_matrix @ vectors_matrix
        print(projected_matrix)
        transposed_matrix = (projected_matrix * self.line_size).transpose()
        lines_end_positions = (transposed_matrix + add_center_matrix).tolist()

        pygame.draw.line(screen, "red", self.center, lines_end_positions[0], 2)
        pygame.draw.line(screen, "green", self.center, lines_end_positions[1], 2)
        pygame.draw.line(screen, "blue", self.center, lines_end_positions[2], 2)