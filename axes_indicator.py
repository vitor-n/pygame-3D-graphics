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
        
        add_center_matrix = np.array(([self.center[0], self.center[1], 0], 
                                      [self.center[0], self.center[1], 0], 
                                      [self.center[0], self.center[1], 0]))
        
        lines_end_positions = (vectors_matrix * -self.line_size + add_center_matrix).tolist()

        pygame.draw.line(screen, "red", self.center, lines_end_positions[0][:2], 2)
        pygame.draw.line(screen, "green", self.center, lines_end_positions[1][:2], 2)
        pygame.draw.line(screen, "blue", self.center, lines_end_positions[2][:2], 2)